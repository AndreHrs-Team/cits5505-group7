-- Demo data for finance and education modules (user_id=1)

-- Insert accounts
INSERT INTO accounts (name, balance, currency, user_id, created_at, updated_at) VALUES
  ('Bank Account', 2000.00, 'USD', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('Cash Wallet', 150.00, 'USD', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert categories
INSERT INTO categories (name, user_id) VALUES
  ('Food', 1),
  ('Salary', 1),
  ('Transport', 1);

-- Insert transactions (assume account_id=1 for Bank Account, account_id=2 for Cash Wallet, category_id=1 for Food, 2 for Salary, 3 for Transport)
INSERT INTO transactions (amount, description, date, account_id, category_id, user_id, created_at, updated_at) VALUES
  (-20.50, 'Lunch at cafe', '2025-05-09 12:30:00', 1, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (3000.00, 'Monthly Salary', '2025-05-01 09:00:00', 1, 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-2.75, 'Bus fare', '2025-05-08 08:00:00', 2, 3, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert education events
INSERT INTO education_event (user_id, title, description, date, time, notes) VALUES
  (1, 'CITS5505 Lecture', 'Web Application Development', '2025-05-10', '09:00:00', 'Lecture on Flask and databases.'),
  (1, 'CITS5508 Lab', 'Data Science Lab', '2025-05-11', '14:00:00', 'Hands-on with pandas.'); 