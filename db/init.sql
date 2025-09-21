-- helper: updated_at
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END$$;

-- periods
CREATE TABLE IF NOT EXISTS periods (
  id SERIAL PRIMARY KEY,
  ym DATE UNIQUE NOT NULL,            -- 1-е число месяца
  is_locked BOOLEAN NOT NULL DEFAULT FALSE
);

-- categories
CREATE TABLE IF NOT EXISTS categories (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  code TEXT UNIQUE,                   -- например credit_card
  parent_id INT REFERENCES categories(id) ON DELETE SET NULL,
  is_system BOOLEAN NOT NULL DEFAULT FALSE
);

-- banks (пока плейсхолдеры)
CREATE TABLE IF NOT EXISTS banks (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  code TEXT UNIQUE
);

-- бюджетные строки (план по категориям на месяц)
CREATE TABLE IF NOT EXISTS budget_lines (
  id BIGSERIAL PRIMARY KEY,
  period_id INT NOT NULL REFERENCES periods(id) ON DELETE RESTRICT,
  category_id INT NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
  bank_id INT REFERENCES banks(id) ON DELETE SET NULL,
  planned_cents BIGINT NOT NULL,
  note TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TRIGGER trg_budget_lines_updated_at
BEFORE UPDATE ON budget_lines
FOR EACH ROW EXECUTE PROCEDURE set_updated_at();

CREATE INDEX IF NOT EXISTS ix_budget_lines_period ON budget_lines(period_id);
CREATE INDEX IF NOT EXISTS ix_budget_lines_category ON budget_lines(category_id);
CREATE INDEX IF NOT EXISTS ix_budget_lines_bank ON budget_lines(bank_id);

-- раскладки внутри строки кредитки
CREATE TABLE IF NOT EXISTS budget_allocations (
  id BIGSERIAL PRIMARY KEY,
  budget_line_id BIGINT NOT NULL REFERENCES budget_lines(id) ON DELETE CASCADE,
  category_id INT NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
  bank_id INT REFERENCES banks(id) ON DELETE SET NULL,
  amount_cents BIGINT NOT NULL,
  note TEXT
);

CREATE INDEX IF NOT EXISTS ix_allocations_line ON budget_allocations(budget_line_id);
CREATE INDEX IF NOT EXISTS ix_allocations_category ON budget_allocations(category_id);
CREATE INDEX IF NOT EXISTS ix_allocations_bank ON budget_allocations(bank_id);

-- доходы месяца (по желанию - можно не использовать сразу)
CREATE TABLE IF NOT EXISTS incomes (
  id BIGSERIAL PRIMARY KEY,
  period_id INT NOT NULL REFERENCES periods(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  planned_cents BIGINT NOT NULL,
  note TEXT
);

CREATE INDEX IF NOT EXISTS ix_incomes_period ON incomes(period_id);

-- стартовые категории
INSERT INTO categories(name, code, is_system) VALUES
  ('Rent', NULL, FALSE),
  ('Groceries', NULL, FALSE),
  ('Subscriptions', NULL, FALSE),
  ('Insurance', NULL, FALSE),
  ('Clothes', NULL, FALSE),
  ('Credit Card', 'credit_card', TRUE)
ON CONFLICT DO NOTHING;

-- стартовые банки - плейсхолдеры
INSERT INTO banks(name, code) VALUES
  ('Bank A', 'bank_a'),
  ('Bank B', 'bank_b'),
  ('Bank C', 'bank_c')
ON CONFLICT DO NOTHING;

-- демо-месяц
INSERT INTO periods(ym, is_locked)
VALUES (DATE '2025-09-01', FALSE)
ON CONFLICT (ym) DO NOTHING;
