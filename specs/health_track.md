# HealthTrack Database Schema

This document describes the database schema for the HealthTrack application. The schema is organized around various health metrics and user data.

## Tables


### 1. activities

This table stores activity data like steps, distance, and calories.

| Field Name       | Type        | Description                                                  |
| ---------------- | ----------- | ------------------------------------------------------------ |
| `id`             | INTEGER     | Primary key, auto-incremented, unique identifier for each activity entry. |
| `user_id`        | INTEGER     | Foreign key referencing `users(id)`, links activity data to a specific user. |
| `import_log_id`  | INTEGER     | Foreign key referencing `import_logs(id)`, indicates which import added this data. |
| `activity_type`  | VARCHAR(50) | Type of activity (e.g., walking, running, cycling).          |
| `value`          | FLOAT       | Numerical value for the activity.                            |
| `unit`           | VARCHAR(10) | Unit of measurement for the value.                           |
| `timestamp`      | DATETIME    | The timestamp when the activity data was recorded.           |
| `total_steps`    | INTEGER     | The total number of steps taken during the activity.         |
| `total_distance` | FLOAT       | The total distance covered in the activity.                  |
| `calories`       | INTEGER     | The total calories burned during the activity.               |
| `data_source`    | VARCHAR(50) | The source from which the data was imported (e.g., Fitbit, Google Fit). |
| `created_at`     | DATETIME    | Timestamp when the record was created.                       |
| `updated_at`     | DATETIME    | Timestamp when the record was last updated.                  |

------

### 2. heart_rates

This table stores heart rate measurements.

| Field Name      | Type        | Description                                                  |
| --------------- | ----------- | ------------------------------------------------------------ |
| `id`            | INTEGER     | Primary key, auto-incremented, unique identifier for each heart rate entry. |
| `user_id`       | INTEGER     | Foreign key referencing `users(id)`, links heart rate data to a specific user. |
| `import_log_id` | INTEGER     | Foreign key referencing `import_logs(id)`, indicates which import added this data. |
| `value`         | INTEGER     | Heart rate value in beats per minute (BPM).                  |
| `unit`          | VARCHAR(10) | Unit of measurement (default: 'bpm').                        |
| `timestamp`     | DATETIME    | The timestamp when the heart rate was measured.              |
| `data_source`   | VARCHAR(50) | The source from which the data was imported.                 |
| `created_at`    | DATETIME    | Timestamp when the record was created.                       |
| `updated_at`    | DATETIME    | Timestamp when the record was last updated.                  |

------

### 3. weights

This table stores weight measurements.

| Field Name      | Type        | Description                                                  |
| --------------- | ----------- | ------------------------------------------------------------ |
| `id`            | INTEGER     | Primary key, auto-incremented, unique identifier for each weight entry. |
| `user_id`       | INTEGER     | Foreign key referencing `users(id)`, links weight data to a specific user. |
| `import_log_id` | INTEGER     | Foreign key referencing `import_logs(id)`, indicates which import added this data. |
| `value`         | FLOAT       | Weight value.                                                |
| `unit`          | VARCHAR(10) | Unit of measurement (e.g., 'kg', 'lb').                      |
| `timestamp`     | DATETIME    | The timestamp when the weight was measured.                  |
| `data_source`   | VARCHAR(50) | The source from which the data was imported.                 |
| `created_at`    | DATETIME    | Timestamp when the record was created.                       |
| `updated_at`    | DATETIME    | Timestamp when the record was last updated.                  |

------

### 4. sleeps

This table stores sleep data.

| Field Name      | Type        | Description                                                  |
| --------------- | ----------- | ------------------------------------------------------------ |
| `id`            | INTEGER     | Primary key, auto-incremented, unique identifier for each sleep entry. |
| `user_id`       | INTEGER     | Foreign key referencing `users(id)`, links sleep data to a specific user. |
| `import_log_id` | INTEGER     | Foreign key referencing `import_logs(id)`, indicates which import added this data. |
| `duration`      | FLOAT       | Total sleep duration in minutes.                             |
| `deep_sleep`    | FLOAT       | Deep sleep duration in minutes.                              |
| `light_sleep`   | FLOAT       | Light sleep duration in minutes.                             |
| `rem_sleep`     | FLOAT       | REM sleep duration in minutes.                               |
| `awake`         | FLOAT       | Awake time during sleep period in minutes.                   |
| `unit`          | VARCHAR(10) | Unit of measurement (default: 'minutes').                    |
| `quality`       | VARCHAR(20) | Sleep quality (e.g., 'good', 'fair', 'poor').               |
| `start_time`    | DATETIME    | The start time of the sleep session.                         |
| `end_time`      | DATETIME    | The end time of the sleep session.                           |
| `timestamp`     | DATETIME    | The timestamp when the sleep data was recorded.              |
| `notes`         | TEXT        | Additional notes about the sleep session.                    |

------

### 5. goals

This table stores user goals for health metrics.

| Field Name          | Type        | Description                                                  |
| ------------------- | ----------- | ------------------------------------------------------------ |
| `id`                | INTEGER     | Primary key, auto-incremented, unique identifier for each goal. |
| `user_id`           | INTEGER     | Foreign key referencing `users(id)`, links the goal to a specific user. |
| `category`          | VARCHAR(50) | Category of the goal (e.g., 'steps', 'weight', 'sleep', 'heart_rate'). |
| `target_value`      | FLOAT       | The target value to achieve.                                 |
| `current_value`     | FLOAT       | The current progress towards the goal.                       |
| `unit`              | VARCHAR(20) | Unit of measurement for the goal.                            |
| `timeframe`         | VARCHAR(20) | Timeframe for achieving the goal (e.g., 'daily', 'weekly', 'monthly'). |
| `start_date`        | DATETIME    | The date when the goal begins.                               |
| `end_date`          | DATETIME    | The date by which the goal should be completed.              |
| `completed`         | BOOLEAN     | Indicates if the goal has been completed.                    |
| `progress_related`  | BOOLEAN     | Indicates if the goal is related to tracking progress over time. |
| `progress_baseline` | FLOAT       | Baseline value for progress calculations.                    |
| `created_at`        | DATETIME    | Timestamp when the goal was created.                         |
| `updated_at`        | DATETIME    | Timestamp when the goal was last updated.                    |

------

### 6. progress

This table tracks progress towards goals.

| Field Name  | Type        | Description                                                  |
| ----------- | ----------- | ------------------------------------------------------------ |
| `id`        | INTEGER     | Primary key, auto-incremented, unique identifier for each progress entry. |
| `user_id`   | INTEGER     | Foreign key referencing `users(id)`, links the progress to a specific user. |
| `goal_id`   | INTEGER     | Foreign key referencing `goals(id)`, links the progress to a specific goal. |
| `value`     | FLOAT       | The progress value.                                          |
| `unit`      | VARCHAR(20) | Unit of measurement for the progress value.                  |
| `timestamp` | DATETIME    | The timestamp when the progress was recorded.                |
| `notes`     | TEXT        | Additional notes about the progress.                         |

------

### 7. achievements

This table defines various achievements that users can earn.

| Field Name        | Type         | Description                                                  |
| ----------------- | ------------ | ------------------------------------------------------------ |
| `id`              | INTEGER      | Primary key, auto-incremented, unique identifier for each achievement. |
| `name`            | VARCHAR(100) | Name of the achievement.                                     |
| `description`     | VARCHAR(255) | Description of the achievement.                              |
| `category`        | VARCHAR(50)  | Category of the achievement (e.g., 'steps', 'weight', 'sleep', 'heart_rate', 'general'). |
| `icon`            | VARCHAR(100) | Icon or image associated with the achievement.               |
| `level`           | VARCHAR(20)  | Level of the achievement (e.g., 'bronze', 'silver', 'gold'). |
| `condition_type`  | VARCHAR(50)  | Type of condition for earning the achievement (e.g., 'streak', 'milestone', 'improvement'). |
| `condition_value` | FLOAT        | Value required to meet the condition.                        |
| `trigger_type`    | VARCHAR(20)  | What triggers the achievement (e.g., 'progress', 'goal', 'combined'). |
| `progress_related` | BOOLEAN     | Indicates if the achievement is related to tracking progress. |
| `goal_related`    | BOOLEAN      | Indicates if the achievement is related to completing goals. |
| `created_at`      | DATETIME     | Timestamp when the achievement was created.                  |

------

### 8. user_achievements

This table tracks which achievements have been earned by users.

| Field Name       | Type     | Description                                                  |
| ---------------- | -------- | ------------------------------------------------------------ |
| `id`             | INTEGER  | Primary key, auto-incremented, unique identifier for each user achievement. |
| `user_id`        | INTEGER  | Foreign key referencing `users(id)`, links the achievement to a specific user. |
| `achievement_id` | INTEGER  | Foreign key referencing `achievements(id)`, links to the specific achievement. |
| `earned_at`      | DATETIME | Timestamp when the achievement was earned.                   |

------

### 9. import_logs

This table logs data import operations.

| Field Name          | Type         | Description                                                  |
| ------------------- | ------------ | ------------------------------------------------------------ |
| `id`                | INTEGER      | Primary key, auto-incremented, unique identifier for each import log. |
| `user_id`           | INTEGER      | Foreign key referencing `users(id)`, links the import to a specific user. |
| `data_source`       | VARCHAR(50)  | The source of the imported data.                             |
| `file_name`         | VARCHAR(255) | Name of the imported file.                                   |
| `status`            | VARCHAR(20)  | Status of the import (e.g., 'success', 'failed', 'processing'). |
| `error_message`     | TEXT         | Error message if the import failed.                          |
| `records_processed` | INTEGER      | Number of records processed during the import.               |
| `created_at`        | DATETIME     | Timestamp when the import was initiated.                     |
| `completed_at`      | DATETIME     | Timestamp when the import was completed.                     |

------

### 10. shared_links

This table stores links for sharing health data with others.

| Field Name          | Type         | Description                                                  |
| ------------------- | ------------ | ------------------------------------------------------------ |
| `id`                | INTEGER      | Primary key, auto-incremented, unique identifier for each shared link. |
| `user_id`           | INTEGER      | Foreign key referencing `users(id)`, links the shared link to a specific user. |
| `share_token`       | VARCHAR(64)  | Unique token used in the share URL.                          |
| `name`              | VARCHAR(100) | Name of the shared link.                                     |
| `expires_at`        | DATETIME     | Expiration date and time for the shared link.                |
| `password_hash`     | VARCHAR(128) | Hash of the password for password-protected links.           |
| `privacy_level`     | VARCHAR(20)  | Privacy level for the shared data (e.g., 'complete', 'overview', 'achievements'). |
| `modules`           | TEXT         | JSON array of modules to include in the shared data.         |
| `date_range_start`  | DATETIME     | Start date for the data range to share.                      |
| `date_range_end`    | DATETIME     | End date for the data range to share.                        |
| `template_type`     | VARCHAR(20)  | Type of template to use for the shared data (e.g., 'medical', 'social'). |
| `personal_message`  | VARCHAR(255) | Personal message included with the shared data.              |
| `theme`             | VARCHAR(20)  | Visual theme for the shared data view.                       |
| `created_at`        | DATETIME     | Timestamp when the shared link was created.                  |
| `last_accessed`     | DATETIME     | Timestamp when the shared link was last accessed.            |
| `access_count`      | INTEGER      | Number of times the shared link has been accessed.           |
| `show_weight`       | BOOLEAN      | Whether to include weight data in the shared data.           |
| `show_heart_rate`   | BOOLEAN      | Whether to include heart rate data in the shared data.       |
| `show_activity`     | BOOLEAN      | Whether to include activity data in the shared data.         |
| `show_sleep`        | BOOLEAN      | Whether to include sleep data in the shared data.            |
| `show_goals`        | BOOLEAN      | Whether to include goals in the shared data.                 |
| `show_achievements` | BOOLEAN      | Whether to include achievements in the shared data.          |
| `one_time_password` | BOOLEAN      | Whether the shared link uses a one-time password.            |
| `password_used`     | BOOLEAN      | Whether the one-time password has been used.                 |

------

### 11. share_access_logs

This table logs access to shared links.

| Field Name      | Type         | Description                                                  |
| --------------- | ------------ | ------------------------------------------------------------ |
| `id`            | INTEGER      | Primary key, auto-incremented, unique identifier for each access log. |
| `share_link_id` | INTEGER      | Foreign key referencing `shared_links(id)`, links the access log to a specific shared link. |
| `accessed_at`   | DATETIME     | Timestamp when the shared link was accessed.                 |
| `ip_address`    | VARCHAR(45)  | IP address of the accessor.                                  |
| `user_agent`    | VARCHAR(255) | User agent of the accessor's browser.                        |
| `successful`    | BOOLEAN      | Whether the access was successful (e.g., correct password).  |
| `access_type`   | VARCHAR(20)  | Type of access (e.g., 'view', 'pdf').                        |

------

## Relationships

- **User** has many: Activities, Heart Rates, Weights, Sleeps, Goals, Progress records, User Achievements, Import Logs, and Shared Links
- **Goal** has many Progress records
- **Achievement** has many User Achievements
- **Import Log** has many: Activities, Heart Rates, Weights, and Sleeps
- **Shared Link** has many Share Access Logs

------

# HealthTrack API Contract

- **Version:** `v1.0`
- **Base URL:** `http://localhost:5000/api`
- **Last Updated:** Apr 17, 2025

This RESTful API powers the HealthTrack Application, allowing users to track personal health data, visualize trends, track goals and achievements, and selectively share data with others. The API supports data from various health platforms including: **Apple Health**, **Google Fit**, **Fitbit**, **Garmin**, and **Samsung Health**.

------


## 1. Dashboard

### GET `/dashboard`

Get dashboard data for the current user.

**Request Headers:**
- `Authorization: Bearer <token>`

**Query Parameters:**
- `days` (optional): Number of days of data to retrieve (default: 7)
- `refresh` (optional): Force refresh of cached data (values: 0 or 1)

**Response:**

- `200 OK` on success

**Example Response:**

```json
{
  "success": true,
  "data": {
    "weight_data": [
      {
        "date": "2024-05-10",
        "value": 70.5,
        "unit": "kg"
      }
    ],
    "heart_rate_data": [
      {
        "date": "2024-05-10",
        "min": 60,
        "max": 120,
        "avg": 75,
        "unit": "bpm"
      }
    ],
    "activity_data": [
      {
        "date": "2024-05-10",
        "steps": 8000
      }
    ],
    "sleep_data": [
      {
        "date": "2024-05-10",
        "duration": 480,
        "durationHours": 8.0,
        "quality": "good"
      }
    ]
  }
}
```

------

### GET `/dashboard/summary`

Get summary statistics for the current user.

**Request Headers:**
- `Authorization: Bearer <token>`

**Query Parameters:**
- `days` (optional): Number of days of data to analyze (default: 7)

**Response:**

- `200 OK` on success

**Example Response:**

```json
{
  "success": true,
  "summary": {
    "weight": {
      "current": 70.5,
      "change": -0.5,
      "unit": "kg"
    },
    "heart_rate": {
      "avg": 72,
      "min": 58,
      "max": 155,
      "unit": "bpm"
    },
    "activity": {
      "avg_steps": 8500,
      "total_steps": 59500
    },
    "sleep": {
      "avg_duration": 7.5,
      "unit": "hours"
    }
  }
}
```

------

### GET `/dashboard/goals-achievements`

Get goals and achievements for the current user.

**Request Headers:**
- `Authorization: Bearer <token>`

**Response:**

- `200 OK` on success

**Example Response:**

```json
{
  "success": true,
  "goals": [
    {
      "id": 1,
      "category": "steps",
      "target_value": 10000,
      "current_value": 8500,
      "unit": "steps",
      "progress": 85
    }
  ],
  "achievements": [
    {
      "id": 2,
      "name": "Step Master",
      "description": "Walk 10,000 steps daily for a week",
      "earned_at": "2024-05-08T10:30:00"
    }
  ]
}
```

------


## 2. Health Data

### GET `/weight`

Get weight data for the current user.

**Request Headers:**
- `Authorization: Bearer <token>`

**Query Parameters:**
- `period` (optional): Time period (values: "daily", "weekly", "monthly", "six_months", "yearly", default: "weekly")
- `start_date` (optional): Start date in format YYYY-MM-DD
- `end_date` (optional): End date in format YYYY-MM-DD

**Response:**

- `200 OK` on success

**Example Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "timestamp": "2024-05-10T08:30:00",
      "value": 70.5,
      "unit": "kg"
    }
  ]
}
```

------

### POST `/weight`

Add a new weight record.

**Request Headers:**
- `Authorization: Bearer <token>`

**Request Body (JSON):**

```json
{
  "value": 0.0,
  "unit": "string",
  "timestamp": "YYYY-MM-DDTHH:MM:SS"
}
```

**Response:**

- `201 Created` on success
- `400 Bad Request` if validation fails

**Example Response:**

```json
{
  "success": true,
  "message": "Weight record added successfully",
  "record": {
    "id": 1,
    "timestamp": "2024-05-10T08:30:00",
    "value": 70.5,
    "unit": "kg"
  }
}
```

------

### GET `/heart-rate`

Get heart rate data for the current user.

**Request Headers:**
- `Authorization: Bearer <token>`

**Query Parameters:**
- `period` (optional): Time period (values: "daily", "weekly", "monthly", "six_months", "yearly", default: "weekly")
- `start_date` (optional): Start date in format YYYY-MM-DD
- `end_date` (optional): End date in format YYYY-MM-DD

**Response:**

- `200 OK` on success

**Example Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "timestamp": "2024-05-10T08:30:00",
      "value": 72,
      "unit": "bpm"
    }
  ]
}
```

------

### POST `/heart-rate`

Add a new heart rate record.

**Request Headers:**
- `Authorization: Bearer <token>`

**Request Body (JSON):**

```json
{
  "value": 0,
  "unit": "string",
  "timestamp": "YYYY-MM-DDTHH:MM:SS"
}
```

**Response:**

- `201 Created` on success
- `400 Bad Request` if validation fails

**Example Response:**

```json
{
  "success": true,
  "message": "Heart rate record added successfully",
  "record": {
    "id": 1,
    "timestamp": "2024-05-10T08:30:00",
    "value": 72,
    "unit": "bpm"
  }
}
```

------

### GET `/activity`

Get activity data for the current user.

**Request Headers:**
- `Authorization: Bearer <token>`

**Query Parameters:**
- `period` (optional): Time period (values: "daily", "weekly", "monthly", "six_months", "yearly", default: "weekly")
- `start_date` (optional): Start date in format YYYY-MM-DD
- `end_date` (optional): End date in format YYYY-MM-DD

**Response:**

- `200 OK` on success

**Example Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "timestamp": "2024-05-10T08:30:00",
      "activity_type": "walking",
      "total_steps": 8000,
      "total_distance": 6.2,
      "calories": 320
    }
  ]
}
```

------

### POST `/activity`

Add a new activity record.

**Request Headers:**
- `Authorization: Bearer <token>`

**Request Body (JSON):**

```json
{
  "activity_type": "string",
  "total_steps": 0,
  "total_distance": 0.0,
  "calories": 0,
  "timestamp": "YYYY-MM-DDTHH:MM:SS"
}
```

**Response:**

- `201 Created` on success
- `400 Bad Request` if validation fails

**Example Response:**

```json
{
  "success": true,
  "message": "Activity record added successfully",
  "record": {
    "id": 1,
    "timestamp": "2024-05-10T08:30:00",
    "activity_type": "walking",
    "total_steps": 8000,
    "total_distance": 6.2,
    "calories": 320
  }
}
```

------

### GET `/sleep`

Get sleep data for the current user.

**Request Headers:**
- `Authorization: Bearer <token>`

**Query Parameters:**
- `period` (optional): Time period (values: "daily", "weekly", "monthly", "six_months", "yearly", default: "weekly")
- `start_date` (optional): Start date in format YYYY-MM-DD
- `end_date` (optional): End date in format YYYY-MM-DD

**Response:**

- `200 OK` on success

**Example Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "start_time": "2024-05-10T23:00:00",
      "end_time": "2024-05-11T07:00:00",
      "duration": 480,
      "deep_sleep": 120,
      "light_sleep": 240,
      "rem_sleep": 100,
      "awake": 20,
      "quality": "good"
    }
  ]
}
```

------

### POST `/sleep`

Add a new sleep record.

**Request Headers:**
- `Authorization: Bearer <token>`

**Request Body (JSON):**

```json
{
  "start_time": "YYYY-MM-DDTHH:MM:SS",
  "end_time": "YYYY-MM-DDTHH:MM:SS",
  "duration": 0,
  "deep_sleep": 0,
  "light_sleep": 0,
  "rem_sleep": 0,
  "awake": 0,
  "quality": "string"
}
```

**Response:**

- `201 Created` on success
- `400 Bad Request` if validation fails

**Example Response:**

```json
{
  "success": true,
  "message": "Sleep record added successfully",
  "record": {
    "id": 1,
    "start_time": "2024-05-10T23:00:00",
    "end_time": "2024-05-11T07:00:00",
    "duration": 480,
    "quality": "good"
  }
}
```

------

## 3. Goals and Achievements

### GET `/goals`

Get goals for the current user.

**Request Headers:**
- `Authorization: Bearer <token>`

**Response:**

- `200 OK` on success

**Example Response:**

```json
{
  "success": true,
  "goals": [
    {
      "id": 1,
      "category": "steps",
      "target_value": 10000,
      "current_value": 8500,
      "unit": "steps",
      "timeframe": "daily",
      "start_date": "2024-05-01",
      "end_date": "2024-05-31",
      "progress": 85,
      "completed": false
    }
  ]
}
```

------

### POST `/goals`

Create a new goal.

**Request Headers:**
- `Authorization: Bearer <token>`

**Request Body (JSON):**

```json
{
  "category": "string",
  "target_value": 0.0,
  "unit": "string",
  "timeframe": "string",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD"
}
```

**Response:**

- `201 Created` on success
- `400 Bad Request` if validation fails

**Example Response:**

```json
{
  "success": true,
  "message": "Goal created successfully",
  "goal": {
    "id": 1,
    "category": "steps",
    "target_value": 10000,
    "unit": "steps",
    "timeframe": "daily"
  }
}
```

------

### PUT `/goals/<goal_id>`

Update an existing goal.

**Request Headers:**
- `Authorization: Bearer <token>`

**Request Body (JSON):**

```json
{
  "target_value": 0.0,
  "current_value": 0.0,
  "end_date": "YYYY-MM-DD",
  "completed": false
}
```

**Response:**

- `200 OK` on success
- `400 Bad Request` if validation fails
- `404 Not Found` if goal doesn't exist

**Example Response:**

```json
{
  "success": true,
  "message": "Goal updated successfully",
  "goal": {
    "id": 1,
    "target_value": 12000,
    "current_value": 9000,
    "progress": 75
  }
}
```

------

### DELETE `/goals/<goal_id>`

Delete a goal.

**Request Headers:**
- `Authorization: Bearer <token>`

**Response:**

- `200 OK` on success
- `404 Not Found` if goal doesn't exist

**Example Response:**

```json
{
  "success": true,
  "message": "Goal deleted successfully"
}
```

------

### GET `/achievements`

Get achievements for the current user.

**Request Headers:**
- `Authorization: Bearer <token>`

**Response:**

- `200 OK` on success

**Example Response:**

```json
{
  "success": true,
  "achievements": [
    {
      "id": 1,
      "name": "Step Master",
      "description": "Walk 10,000 steps daily for a week",
      "category": "steps",
      "icon": "steps-icon",
      "level": "gold",
      "earned_at": "2024-05-10T18:30:00"
    }
  ]
}
```

------

## 4. Data Import/Export

### POST `/upload`

Upload health data from a file.

**Request Headers:**
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

**Request Body:**
- `file`: File to upload
- `dataSource`: Source of the data (e.g., "fitbit", "apple_health", "google_fit")

**Response:**

- `200 OK` on success
- `400 Bad Request` if file validation fails

**Example Response:**

```json
{
  "success": true,
  "message": "File uploaded and processed successfully",
  "import_log_id": 123
}
```

------

### GET `/import_history`

Get import history for the current user.

**Request Headers:**
- `Authorization: Bearer <token>`

**Response:**

- `200 OK` on success

**Example Response:**

```json
{
  "success": true,
  "import_logs": [
    {
      "id": 123,
      "data_source": "fitbit",
      "file_name": "fitbit_export_2024-05-10.csv",
      "status": "success",
      "records_processed": 150,
      "created_at": "2024-05-10T15:30:00"
    }
  ]
}
```

------

### GET `/export_data`

Export user data in CSV/JSON format.

**Request Headers:**
- `Authorization: Bearer <token>`

**Query Parameters:**
- `format` (optional): Export format (values: "csv", "json", default: "csv")
- `data_types` (optional): Comma-separated list of data types to export (default: all)

**Response:**

- `200 OK` on success with file download

------

## 5. Data Sharing

### GET `/share/links`

Get all share links for the current user.

**Request Headers:**
- `Authorization: Bearer <token>`

**Response:**

- `200 OK` on success

**Example Response:**

```json
{
  "success": true,
  "share_links": [
    {
      "id": 1,
      "share_token": "abc123def456",
      "name": "Doctor Visit",
      "expires_at": "2024-06-10T00:00:00",
      "has_password": true,
      "template_type": "medical",
      "created_at": "2024-05-10T15:30:00",
      "access_count": 3
    }
  ]
}
```

------

### POST `/share/links`

Create a new share link.

**Request Headers:**
- `Authorization: Bearer <token>`

**Request Body (JSON):**

```json
{
  "name": "string",
  "privacy_level": "string",
  "modules": ["dashboard", "heartrate", "activity", "weight", "sleep", "goals", "achievements"],
  "template_type": "string",
  "expiration_days": 0,
  "password": "string",
  "personal_message": "string",
  "days": 30
}
```

**Response:**

- `200 OK` on success
- `400 Bad Request` if validation fails

**Example Response:**

```json
{
  "success": true,
  "share_link": {
    "id": 1,
    "share_token": "abc123def456",
    "url": "/share/view/abc123def456"
  }
}
```

------

### DELETE `/share/links/<share_token>`

Delete a share link.

**Request Headers:**
- `Authorization: Bearer <token>`

**Response:**

- `200 OK` on success
- `404 Not Found` if share link doesn't exist

**Example Response:**

```json
{
  "success": true,
  "message": "Share link deleted successfully"
}
```

------

### GET `/share/links/<share_token>`

Get details for a specific share link.

**Request Headers:**
- `Authorization: Bearer <token>`

**Response:**

- `200 OK` on success
- `404 Not Found` if share link doesn't exist

**Example Response:**

```json
{
  "success": true,
  "share_link": {
    "id": 1,
    "share_token": "abc123def456",
    "name": "Doctor Visit",
    "expires_at": "2024-06-10T00:00:00",
    "has_password": true,
    "privacy_level": "overview",
    "modules": ["dashboard", "heartrate", "weight"],
    "template_type": "medical",
    "personal_message": "For my annual checkup",
    "created_at": "2024-05-10T15:30:00"
  }
}
```

------

## 6. Error Responses

All endpoints may return the following error responses:

### `400 Bad Request`

```json
{
  "success": false,
  "message": "Error message describing the problem",
  "errors": {
    "field_name": "Specific error for this field"
  }
}
```

### `401 Unauthorized`

```json
{
  "success": false,
  "message": "Authentication required"
}
```

### `403 Forbidden`

```json
{
  "success": false,
  "message": "You don't have permission to access this resource"
}
```

### `404 Not Found`

```json
{
  "success": false,
  "message": "Resource not found"
}
```

### `500 Internal Server Error`

```json
{
  "success": false,
  "message": "An unexpected error occurred"
}
``` 
