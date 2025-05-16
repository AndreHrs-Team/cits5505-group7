-- Demo data for finance and education modules (user_id=1)

-- Insert accounts
INSERT INTO accounts (name, balance, currency, user_id, created_at, updated_at) VALUES
  ('Bank Account', 2000.00, 'USD', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('Cash Wallet', 150.00, 'USD', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('Credit Card', -500.00, 'USD', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('Savings Account', 8000.00, 'USD', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);


-- Insert categories
INSERT INTO categories (name, user_id) VALUES
  ('Food', 1),
  ('Salary', 1),
  ('Transport', 1),
  ('Entertainment', 1),
  ('Utilities', 1),
  ('Investment', 1),
  ('Gift', 1);

-- Insert transactions (assume account_id=1 for Bank Account, account_id=2 for Cash Wallet, category_id=1 for Food, 2 for Salary, 3 for Transport)
INSERT INTO transactions (amount, description, date, account_id, category_id, user_id, created_at, updated_at) VALUES
  (-173.19, 'Movie', '2025-04-15 00:00:00', 2, 7, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (207.14, 'Freelance', '2025-04-16 00:00:00', 4, 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-60.61, 'Gift', '2025-04-17 00:00:00', 1, 4, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-174.7, 'Movie', '2025-04-18 00:00:00', 2, 7, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-97.16, 'Gift', '2025-04-19 00:00:00', 2, 3, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (656.3, 'Freelance', '2025-04-20 00:00:00', 1, 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-46.87, 'Lunch', '2025-04-21 00:00:00', 2, 4, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-157.43, 'Bus fare', '2025-04-22 00:00:00', 2, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-163.09, 'Shopping', '2025-04-23 00:00:00', 2, 3, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-104.46, 'Bus fare', '2025-04-24 00:00:00', 2, 7, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-54.76, 'Electricity', '2025-04-25 00:00:00', 2, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-98.18, 'Bus fare', '2025-04-26 00:00:00', 2, 4, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-43.53, 'Coffee', '2025-04-27 00:00:00', 2, 3, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-190.57, 'Gift', '2025-04-28 00:00:00', 1, 7, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (1643.64, 'Freelance', '2025-04-29 00:00:00', 1, 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-70.12, 'Shopping', '2025-04-30 00:00:00', 1, 7, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-36.36, 'Coffee', '2025-05-01 00:00:00', 2, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-61.34, 'Bus fare', '2025-05-02 00:00:00', 1, 4, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-146.7, 'Coffee', '2025-05-03 00:00:00', 1, 4, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2846.51, 'Investment return', '2025-05-04 00:00:00', 4, 6, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-23.98, 'Electricity', '2025-05-05 00:00:00', 1, 3, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-157.36, 'Coffee', '2025-05-06 00:00:00', 2, 3, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2716.48, 'Stock dividend', '2025-05-07 00:00:00', 4, 6, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (702.78, 'Salary', '2025-05-08 00:00:00', 1, 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-77.42, 'Coffee', '2025-05-09 00:00:00', 2, 7, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-24.15, 'Coffee', '2025-05-10 00:00:00', 1, 7, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-9.84, 'Gift', '2025-05-11 00:00:00', 2, 5, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-58.58, 'Shopping', '2025-05-12 00:00:00', 2, 7, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-172.05, 'Movie', '2025-05-13 00:00:00', 2, 7, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (513.82, 'Salary', '2025-05-14 00:00:00', 4, 6, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-147.96, 'Movie', '2025-05-15 00:00:00', 1, 4, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (1497.04, 'Freelance', '2025-05-16 00:00:00', 1, 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-126.06, 'Shopping', '2025-05-17 00:00:00', 2, 3, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-62.97, 'Movie', '2025-05-18 00:00:00', 2, 5, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-129.21, 'Lunch', '2025-05-19 00:00:00', 2, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (1552.67, 'Salary', '2025-05-20 00:00:00', 4, 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-22.26, 'Electricity', '2025-05-21 00:00:00', 1, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (-42.61, 'Electricity', '2025-05-22 00:00:00', 1, 7, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);


-- Insert education events
INSERT INTO education_event (user_id, title, description, date, time, notes) VALUES
  (1, 'CITS5505 Lecture', 'Web Application Development', '2025-05-10', '09:00:00', 'Lecture on Flask and databases.'),
  (1, 'CITS5508 Lab', 'Data Science Lab', '2025-05-11', '14:00:00', 'Hands-on with pandas.'); 


