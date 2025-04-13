## 1. Table Definitions

------

### **1. `daily_activities` Table**

Tracks aggregated daily fitness activity summaries.

| Column                     | Type                   | Constraints                                           | Description                                                  | Default           |
| -------------------------- | ---------------------- | ----------------------------------------------------- | ------------------------------------------------------------ | ----------------- |
| id                         | INTEGER                | PRIMARY KEY AUTOINCREMENT                             | Unique identifier for the daily log.                         |                   |
| user_id                    | INTEGER                | NOT NULL                                              | Identifier for the associated user/entity (managed externally). |                   |
| date                       | DATE                   | NOT NULL                                              | The specific date this activity summary applies to.          |                   |
| total_steps                | INTEGER                |                                                       | Total steps taken on this day.                               | NULL              |
| total_distance             | FLOAT                  |                                                       | Total distance covered (e.g., in km). Base unit defined by app. | NULL              |
| tracker_distance           | FLOAT                  |                                                       | Distance recorded automatically by tracker (if applicable).  | NULL              |
| logged_activities_distance | FLOAT                  |                                                       | Distance from manually logged exercises (e.g., runs).        | NULL              |
| very_active_minutes        | INTEGER                |                                                       | Minutes spent in high-intensity activity.                    | NULL              |
| fairly_active_minutes      | INTEGER                |                                                       | Minutes spent in moderate-intensity activity.                | NULL              |
| lightly_active_minutes     | INTEGER                |                                                       | Minutes spent in low-intensity activity.                     | NULL              |
| sedentary_minutes          | INTEGER                |                                                       | Minutes spent sedentary.                                     | NULL              |
| calories                   | INTEGER                |                                                       | Estimated total calories burned on this day.                 | NULL              |
| created_at                 | TIMESTAMP              | NOT NULL                                              | Timestamp when this log entry was created.                   | CURRENT_TIMESTAMP |
| updated_at                 | TIMESTAMP              | NOT NULL                                              | Timestamp when this log entry was last updated. (App logic). | CURRENT_TIMESTAMP |
| *Constraint*               | UNIQUE (user_id, date) | Ensures only one summary log per user/entity per day. |                                                              |                   |

------

### **2. `sleep_logs` Table**

Records details about sleep sessions.

| Column               | Type      | Constraints               | Description                                                  | Default           |
| -------------------- | --------- | ------------------------- | ------------------------------------------------------------ | ----------------- |
| id                   | INTEGER   | PRIMARY KEY AUTOINCREMENT | Unique identifier for the sleep log.                         |                   |
| user_id              | INTEGER   | NOT NULL                  | Identifier for the associated user/entity (managed externally). |                   |
| date                 | DATE      | NOT NULL                  | Date the sleep session *ended* on (convention).              |                   |
| start_time           | TIMESTAMP |                           | Exact time sleep session started.                            | NULL              |
| end_time             | TIMESTAMP |                           | Exact time sleep session ended.                              | NULL              |
| total_sleep_records  | INTEGER   |                           | Number of distinct sleep periods recorded (if tracker provides). | NULL              |
| total_minutes_asleep | INTEGER   |                           | Total time spent actually asleep during the session.         | NULL              |
| total_time_in_bed    | INTEGER   |                           | Total time from start_time to end_time.                      | NULL              |
| sleep_efficiency     | INTEGER   |                           | Sleep efficiency percentage ((total_minutes_asleep / total_time_in_bed) * 100). | NULL              |
| created_at           | TIMESTAMP | NOT NULL                  | Timestamp when this log entry was created.                   | CURRENT_TIMESTAMP |
| updated_at           | TIMESTAMP | NOT NULL                  | Timestamp when this log entry was last updated. (App logic). | CURRENT_TIMESTAMP |

------

### **3. `sleep_stages` Table**

Stores breakdown of time spent in different sleep stages for a specific sleep log.

| Column       | Type        | Constraints                                      | Description                                                | Default           |
| ------------ | ----------- | ------------------------------------------------ | ---------------------------------------------------------- | ----------------- |
| id           | INTEGER     | PRIMARY KEY AUTOINCREMENT                        | Unique identifier for the sleep stage entry.               |                   |
| sleep_log_id | INTEGER     | NOT NULL, FK -> sleep_logs(id) ON DELETE CASCADE | Links to the parent sleep log session.                     |                   |
| stage        | VARCHAR(20) | NOT NULL, CHECK(...)                             | The type of sleep stage ('deep', 'light', 'rem', 'awake'). |                   |
| minutes      | INTEGER     | NOT NULL                                         | Duration spent in this stage in minutes.                   |                   |
| created_at   | TIMESTAMP   | NOT NULL                                         | Timestamp when this stage entry was created.               | CURRENT_TIMESTAMP |

------

### **4. `heart_rate_logs` Table**

Stores individual time-series heart rate measurements.

| Column     | Type        | Constraints               | Description                                                  | Default           |
| ---------- | ----------- | ------------------------- | ------------------------------------------------------------ | ----------------- |
| id         | INTEGER     | PRIMARY KEY AUTOINCREMENT | Unique identifier for the heart rate reading.                |                   |
| user_id    | INTEGER     | NOT NULL                  | Identifier for the associated user/entity (managed externally). |                   |
| datetime   | TIMESTAMP   | NOT NULL                  | Precise timestamp of the heart rate measurement.             |                   |
| value      | INTEGER     | NOT NULL                  | Heart rate value in beats per minute (BPM).                  |                   |
| zone       | VARCHAR(20) |                           | Calculated heart rate zone (e.g., 'Fat Burn', 'Cardio', 'Peak'). | NULL              |
| created_at | TIMESTAMP   | NOT NULL                  | Timestamp when this reading was recorded in the system.      | CURRENT_TIMESTAMP |

------

### **5. `heart_rate_summary` Table**

Stores aggregated daily heart rate statistics, denormalized for performance.

| Column               | Type                   | Constraints                                                  | Description                                                  | Default           |
| -------------------- | ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ----------------- |
| id                   | INTEGER                | PRIMARY KEY AUTOINCREMENT                                    | Unique identifier for the daily summary.                     |                   |
| user_id              | INTEGER                | NOT NULL                                                     | Identifier for the associated user/entity (managed externally). |                   |
| date                 | DATE                   | NOT NULL                                                     | The specific date this summary applies to.                   |                   |
| resting_heart_rate   | INTEGER                |                                                              | Calculated resting heart rate for the day (BPM).             | NULL              |
| max_heart_rate       | INTEGER                |                                                              | Maximum heart rate recorded during the day (BPM).            | NULL              |
| min_heart_rate       | INTEGER                |                                                              | Minimum heart rate recorded during the day (BPM).            | NULL              |
| avg_heart_rate       | INTEGER                |                                                              | Average heart rate throughout the day (BPM).                 | NULL              |
| out_of_range_minutes | INTEGER                |                                                              | Total minutes spent with heart rate below the defined zones. | NULL              |
| fat_burn_minutes     | INTEGER                |                                                              | Total minutes spent in the 'Fat Burn' zone.                  | NULL              |
| cardio_minutes       | INTEGER                |                                                              | Total minutes spent in the 'Cardio' zone.                    | NULL              |
| peak_minutes         | INTEGER                |                                                              | Total minutes spent in the 'Peak' zone.                      | NULL              |
| created_at           | TIMESTAMP              | NOT NULL                                                     | Timestamp when this summary was created/calculated.          | CURRENT_TIMESTAMP |
| updated_at           | TIMESTAMP              | NOT NULL                                                     | Timestamp when this summary was last updated. (App logic).   | CURRENT_TIMESTAMP |
| *Constraint*         | UNIQUE (user_id, date) | Ensures only one heart rate summary per user/entity per day. |                                                              |                   |

------

### **6. `weight_logs` Table**

Tracks weight and related body metrics over time.

| Column           | Type      | Constraints               | Description                                                  | Default           |
| ---------------- | --------- | ------------------------- | ------------------------------------------------------------ | ----------------- |
| id               | INTEGER   | PRIMARY KEY AUTOINCREMENT | Unique identifier for the weight log entry.                  |                   |
| user_id          | INTEGER   | NOT NULL                  | Identifier for the associated user/entity (managed externally). |                   |
| date             | DATE      | NOT NULL                  | Date of the weight measurement.                              |                   |
| time             | TIME      |                           | Optional time of the weight measurement.                     | NULL              |
| weight_kg        | FLOAT     | NOT NULL                  | Weight measured in kilograms (base unit).                    |                   |
| bmi              | FLOAT     |                           | Calculated Body Mass Index (optional, calculated by app).    | NULL              |
| fat_percent      | FLOAT     |                           | Body fat percentage (optional, from scale or manual input).  | NULL              |
| is_manual_report | BOOLEAN   |                           | Flag indicating if the entry was manually added vs. synced from a device. | TRUE              |
| created_at       | TIMESTAMP | NOT NULL                  | Timestamp when this log entry was created.                   | CURRENT_TIMESTAMP |
| updated_at       | TIMESTAMP | NOT NULL                  | Timestamp when this log entry was last updated. (App logic). | CURRENT_TIMESTAMP |

------

### **7. `exercise_definitions` Table**

Standardizes exercise types used in logs and routines.

| Column       | Type         | Constraints               | Description                                                  | Default |
| ------------ | ------------ | ------------------------- | ------------------------------------------------------------ | ------- |
| id           | INTEGER      | PRIMARY KEY AUTOINCREMENT | Unique identifier for the exercise definition.               |         |
| name         | VARCHAR(100) | NOT NULL, UNIQUE          | Standardized name of the exercise (e.g., "Running", "Bench Press"). |         |
| category     | VARCHAR(50)  |                           | Exercise category (e.g., 'Cardio', 'Strength', 'Flexibility'). | NULL    |
| description  | TEXT         |                           | Optional description of the exercise.                        | NULL    |
| default_unit | VARCHAR(20)  |                           | Typical unit for measuring this exercise (e.g., 'minutes', 'reps', 'km'). | NULL    |

Export to Sheets

------

### **8. `exercise_logs` Table**

Records specific workout sessions.

| Column                 | Type        | Constraints                                       | Description                                                  | Default           |
| ---------------------- | ----------- | ------------------------------------------------- | ------------------------------------------------------------ | ----------------- |
| id                     | INTEGER     | PRIMARY KEY AUTOINCREMENT                         | Unique identifier for the exercise log entry.                |                   |
| user_id                | INTEGER     | NOT NULL                                          | Identifier for the associated user/entity (managed externally). |                   |
| date                   | DATE        | NOT NULL                                          | Date the exercise was performed.                             |                   |
| start_time             | TIME        |                                                   | Optional start time of the workout.                          | NULL              |
| end_time               | TIME        |                                                   | Optional end time of the workout.                            | NULL              |
| exercise_definition_id | INTEGER     | FK -> exercise_definitions(id) ON DELETE SET NULL | Links to the standardized exercise definition.               | NULL              |
| exercise_type_legacy   | VARCHAR(50) |                                                   | (Optional) Store original free text if migrating or if definition not found. | NULL              |
| duration_minutes       | INTEGER     | NOT NULL                                          | Duration of the exercise session in minutes.                 |                   |
| calories_burned        | INTEGER     |                                                   | Estimated calories burned during the session (optional).     | NULL              |
| avg_heart_rate         | INTEGER     |                                                   | Average heart rate during the session (optional, BPM).       | NULL              |
| max_heart_rate         | INTEGER     |                                                   | Maximum heart rate during the session (optional, BPM).       | NULL              |
| distance_km            | FLOAT       |                                                   | Distance covered in kilometers (optional).                   | NULL              |
| notes                  | TEXT        |                                                   | User's personal notes about the workout session (optional).  | NULL              |
| routine_id             | INTEGER     | FK -> routines(id) ON DELETE SET NULL             | Optional link to a predefined routine that was followed for this session. | NULL              |
| created_at             | TIMESTAMP   | NOT NULL                                          | Timestamp when this log entry was created.                   | CURRENT_TIMESTAMP |
| updated_at             | TIMESTAMP   | NOT NULL                                          | Timestamp when this log entry was last updated. (App logic). | CURRENT_TIMESTAMP |

------

### **9. `routines` Table**

Stores defined workout routines.

| Column      | Type         | Constraints               | Description                                                  | Default           |
| ----------- | ------------ | ------------------------- | ------------------------------------------------------------ | ----------------- |
| id          | INTEGER      | PRIMARY KEY AUTOINCREMENT | Unique identifier for the routine.                           |                   |
| user_id     | INTEGER      | NOT NULL                  | Identifier for the associated user/entity (managed externally). |                   |
| name        | VARCHAR(100) | NOT NULL                  | Name of the workout routine (e.g., "Upper Body Day").        |                   |
| description | TEXT         |                           | Optional description of the routine.                         | NULL              |
| created_at  | TIMESTAMP    | NOT NULL                  | Timestamp when the routine was created.                      | CURRENT_TIMESTAMP |
| updated_at  | TIMESTAMP    | NOT NULL                  | Timestamp when the routine was last updated. (App logic).    | CURRENT_TIMESTAMP |

------

### **10. `routine_exercises` Table**

Links specific exercises (standardized) to a routine, detailing sets, reps, weight, etc.

| Column                 | Type      | Constraints                                                | Description                                                  | Default           |
| ---------------------- | --------- | ---------------------------------------------------------- | ------------------------------------------------------------ | ----------------- |
| id                     | INTEGER   | PRIMARY KEY AUTOINCREMENT                                  | Unique identifier for this entry within a routine.           |                   |
| routine_id             | INTEGER   | NOT NULL, FK -> routines(id) ON DELETE CASCADE             | Links to the parent routine.                                 |                   |
| exercise_definition_id | INTEGER   | NOT NULL, FK -> exercise_definitions(id) ON DELETE CASCADE | Links to the standardized exercise definition.               |                   |
| sets                   | INTEGER   |                                                            | Number of sets (for strength training).                      | NULL              |
| reps                   | INTEGER   |                                                            | Number of repetitions per set.                               | NULL              |
| weight_kg              | FLOAT     |                                                            | Weight used in kilograms (for strength training).            | NULL              |
| duration_minutes       | INTEGER   |                                                            | Duration for timed exercises (e.g., plank).                  | NULL              |
| distance_km            | FLOAT     |                                                            | Target distance for distance-based exercises within the routine. | NULL              |
| order_in_routine       | INTEGER   | NOT NULL                                                   | Sequence number determining the order of exercises within the routine. |                   |
| notes                  | TEXT      |                                                            | Optional notes specific to this exercise within the routine. | NULL              |
| created_at             | TIMESTAMP | NOT NULL                                                   | Timestamp when this exercise was added to the routine.       | CURRENT_TIMESTAMP |

------

### **11. `goals` Table**

Tracks defined fitness and health goals.

| Column          | Type         | Constraints               | Description                                                  | Default           |
| --------------- | ------------ | ------------------------- | ------------------------------------------------------------ | ----------------- |
| id              | INTEGER      | PRIMARY KEY AUTOINCREMENT | Unique identifier for the goal.                              |                   |
| user_id         | INTEGER      | NOT NULL                  | Identifier for the associated user/entity (managed externally). |                   |
| name            | VARCHAR(150) |                           | User-defined name or title for the goal (e.g., "Run a 5k").  | NULL              |
| goal_type       | VARCHAR(50)  | NOT NULL                  | Category of the goal (e.g., 'steps', 'sleep', 'weight', 'exercise_duration', 'custom'). |                   |
| target_value    | FLOAT        | NOT NULL                  | The numerical target to achieve.                             |                   |
| target_unit     | VARCHAR(20)  |                           | Unit associated with the target value (e.g., 'steps', 'minutes', 'kg', '%'). | NULL              |
| start_value     | FLOAT        |                           | Value at the start of the goal tracking period (optional).   | NULL              |
| current_value   | FLOAT        |                           | Current progress towards the target. (Needs application logic to update). | NULL              |
| start_date      | DATE         | NOT NULL                  | Date when the goal tracking begins.                          |                   |
| target_date     | DATE         |                           | Optional target completion date for the goal.                | NULL              |
| is_completed    | BOOLEAN      |                           | Flag indicating if the goal has been achieved. (App logic updates this). | FALSE             |
| completion_date | DATE         |                           | Date when the goal was marked as completed (optional).       | NULL              |
| created_at      | TIMESTAMP    | NOT NULL                  | Timestamp when the goal was created.                         | CURRENT_TIMESTAMP |
| updated_at      | TIMESTAMP    | NOT NULL                  | Timestamp when the goal was last updated (e.g., progress update). (App logic). | CURRENT_TIMESTAMP |

------

### **12. `achievements` Table**

Defines the available achievements or badges related to health tracking. Typically pre-populated.

| Column           | Type         | Constraints               | Description                                                  | Default           |
| ---------------- | ------------ | ------------------------- | ------------------------------------------------------------ | ----------------- |
| id               | INTEGER      | PRIMARY KEY AUTOINCREMENT | Unique identifier for the achievement definition.            |                   |
| name             | VARCHAR(100) | NOT NULL, UNIQUE          | Name of the achievement (e.g., "Daily Steps Gold").          |                   |
| description      | TEXT         | NOT NULL                  | Description explaining how to earn the achievement.          |                   |
| badge_icon       | VARCHAR(255) |                           | Path or URL to the icon representing the badge (optional).   | NULL              |
| achievement_type | VARCHAR(50)  | NOT NULL                  | Category of achievement ('steps', 'sleep', 'streak', 'weight', 'exercise'). |                   |
| threshold_value  | FLOAT        |                           | Numerical threshold needed to earn the achievement (if applicable). | NULL              |
| threshold_unit   | VARCHAR(20)  |                           | Unit associated with the threshold value (e.g., 'steps', 'days', '%'). | NULL              |
| created_at       | TIMESTAMP    | NOT NULL                  | Timestamp when this achievement definition was created.      | CURRENT_TIMESTAMP |

------

### **13. `user_achievements` Table**

Tracks earned achievements related to health tracking.

| Column         | Type                             | Constraints                                                  | Description                                                  | Default           |
| -------------- | -------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ----------------- |
| id             | INTEGER                          | PRIMARY KEY AUTOINCREMENT                                    | Unique identifier for the earned achievement record.         |                   |
| user_id        | INTEGER                          | NOT NULL                                                     | Identifier for the associated user/entity (managed externally). |                   |
| achievement_id | INTEGER                          | NOT NULL, FK -> achievements(id) ON DELETE CASCADE           | Links to the specific achievement definition that was earned. |                   |
| date_achieved  | TIMESTAMP                        | NOT NULL                                                     | Timestamp when the criteria for the achievement were met.    | CURRENT_TIMESTAMP |
| *Constraint*   | UNIQUE (user_id, achievement_id) | Ensures an entity typically earns a specific achievement type only once. (Remove if re-earning allowed). |                                                              |                   |

------

### **14. `data_imports` Table**

Tracks history of health data import operations.

| Column        | Type         | Constraints               | Description                                                  | Default           |
| ------------- | ------------ | ------------------------- | ------------------------------------------------------------ | ----------------- |
| id            | INTEGER      | PRIMARY KEY AUTOINCREMENT | Unique identifier for the import record.                     |                   |
| user_id       | INTEGER      | NOT NULL                  | Identifier for the associated user/entity (managed externally). |                   |
| import_type   | VARCHAR(50)  | NOT NULL                  | Method of import ('manual', 'csv', 'api').                   |                   |
| source        | VARCHAR(100) |                           | Source identifier (e.g., filename, API name like 'Fitbit').  | NULL              |
| record_count  | INTEGER      | NOT NULL                  | Number of records processed or attempted in the import.      |                   |
| status        | VARCHAR(20)  | NOT NULL, CHECK(...)      | Status of the import ('pending', 'completed', 'failed', 'completed_with_errors'). |                   |
| error_message | TEXT         |                           | Details of any errors encountered during import (optional).  | NULL              |
| import_date   | TIMESTAMP    | NOT NULL                  | Timestamp when the import process was initiated.             | CURRENT_TIMESTAMP |

Export to Sheets

------

### **15. `recommendations` Table**

Stores generated health/fitness recommendations.

| Column              | Type        | Constraints               | Description                                                  | Default           |
| ------------------- | ----------- | ------------------------- | ------------------------------------------------------------ | ----------------- |
| id                  | INTEGER     | PRIMARY KEY AUTOINCREMENT | Unique identifier for the recommendation record.             |                   |
| user_id             | INTEGER     | NOT NULL                  | Identifier for the associated user/entity (managed externally). |                   |
| recommendation_text | TEXT        | NOT NULL                  | The actual text of the recommendation message.               |                   |
| recommendation_type | VARCHAR(50) |                           | Category (e.g., 'sleep', 'activity', 'nutrition', 'goal_related'). | NULL              |
| related_item_type   | VARCHAR(50) |                           | Optional: Table name of data that triggered it (e.g., 'sleep_log', 'goal'). | NULL              |
| related_item_id     | INTEGER     |                           | Optional: ID of the record in related_item_type table.       | NULL              |
| created_at          | TIMESTAMP   | NOT NULL                  | Timestamp indicating when the recommendation was generated.  | CURRENT_TIMESTAMP |
| is_viewed           | BOOLEAN     |                           | Has the recommendation been seen?                            | FALSE             |
| viewed_at           | TIMESTAMP   |                           | Timestamp when first viewed.                                 | NULL              |
| is_actioned         | BOOLEAN     |                           | Has the recommendation been actioned/dismissed?              | FALSE             |
| actioned_at         | TIMESTAMP   |                           | Timestamp when actioned/dismissed.                           | NULL              |
| priority            | VARCHAR(20) |                           | Optional priority ('low', 'medium', 'high').                 | 'medium'          |

---



## 2. API Contract

**Base URL**: /api/v1

**Version**: 1.0.0

**Authentication**: Session-based (Flask-Login). All endpoints except /achievements and /exercises/definitions require a valid session cookie from /auth/login.

**Content-Type**: application/json for all requests/responses unless specified (e.g., multipart/form-data for imports).

**Date Format**: YYYY-MM-DD for dates, ISO 8601 (YYYY-MM-DDThh:mm:ssZ) for datetimes.

**Error Handling**: Responses include success (boolean), data (object or null), message (string), and optional error (string).

---

### **1. Daily Activities**

Manage daily activity summaries.

#### POST /api/v1/users/{user_id}/activities/daily

Create or update a daily activity summary for a specific date.

**Path Parameters**:

- user_id (integer, required): User ID.

**Request Body**:

json

```json
{
  "date": "2025-04-14", *// Required, YYYY-MM-DD*
  "total_steps": 9800, *// Optional, integer*
  "total_distance": 7.5, *// Optional, float, km*
  "tracker_distance": 7.0, *// Optional, float, km*
  "logged_activities_distance": 0.5, *// Optional, float, km*
  "very_active_minutes": 30, *// Optional, integer*
  "fairly_active_minutes": 55, *// Optional, integer*
  "lightly_active_minutes": 110, *// Optional, integer*
  "sedentary_minutes": 750, *// Optional, integer*
  "calories": 2700 *// Optional, integer*
}
```

**Responses**:

- **201 Created** (New record):

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 150,
      "user_id": 123,
      "date": "2025-04-14",
      "total_steps": 9800,
      "total_distance": 7.5,
      "tracker_distance": 7.0,
      "logged_activities_distance": 0.5,
      "very_active_minutes": 30,
      "fairly_active_minutes": 55,
      "lightly_active_minutes": 110,
      "sedentary_minutes": 750,
      "calories": 2700,
      "created_at": "2025-04-14T10:00:00Z",
      "updated_at": "2025-04-14T10:00:00Z"
    },
    "message": "Daily activity summary created successfully."
  }
  ```

- **200 OK** (Updated record):

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 145,
      "user_id": 123,
      "date": "2025-04-14",
      "total_steps": 9800,
      "total_distance": 7.5,
      "tracker_distance": 7.0,
      "logged_activities_distance": 0.5,
      "very_active_minutes": 30,
      "fairly_active_minutes": 55,
      "lightly_active_minutes": 110,
      "sedentary_minutes": 750,
      "calories": 2700,
      "created_at": "2025-04-13T09:00:00Z",
      "updated_at": "2025-04-14T10:05:00Z"
    },
    "message": "Daily activity summary updated successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/activities/daily

Retrieve a list of daily activity summaries.

**Path Parameters**:

- user_id (integer, required): User ID.

**Query Parameters**:

- start_date (string, optional): YYYY-MM-DD.
- end_date (string, optional): YYYY-MM-DD.
- limit (integer, optional): Number of records to return.
- offset (integer, optional): Number of records to skip.

**Response**:

- **200 OK**:

  json

  CollapseWrapCopy

  ```json
  {
    "success": true,
    "data": [
      {
        "id": 145,
        "user_id": 123,
        "date": "2025-04-14",
        "total_steps": 9800,
        "total_distance": 7.5,
        "tracker_distance": 7.0,
        "logged_activities_distance": 0.5,
        "very_active_minutes": 30,
        "fairly_active_minutes": 55,
        "lightly_active_minutes": 110,
        "sedentary_minutes": 750,
        "calories": 2700,
        "created_at": "2025-04-13T09:00:00Z",
        "updated_at": "2025-04-14T10:05:00Z"
      }
    ],
    "message": "Daily activity summaries retrieved successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/activities/daily/{date}

Retrieve a daily activity summary for a specific date.

**Path Parameters**:

- user_id (integer, required): User ID.
- date (string, required): YYYY-MM-DD.

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 145,
      "user_id": 123,
      "date": "2025-04-14",
      "total_steps": 9800,
      "total_distance": 7.5,
      "tracker_distance": 7.0,
      "logged_activities_distance": 0.5,
      "very_active_minutes": 30,
      "fairly_active_minutes": 55,
      "lightly_active_minutes": 110,
      "sedentary_minutes": 750,
      "calories": 2700,
      "created_at": "2025-04-13T09:00:00Z",
      "updated_at": "2025-04-14T10:05:00Z"
    },
    "message": "Daily activity summary retrieved successfully."
  }
  ```

#### PUT /api/v1/users/{user_id}/activities/daily/{date}

Fully update a daily activity summary for a specific date.

**Path Parameters**:

- user_id (integer, required): User ID.
- date (string, required): YYYY-MM-DD.

**Request Body**: (Same as POST /activities/daily)

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 145,
      "user_id": 123,
      "date": "2025-04-14",
      "total_steps": 9999,
      "total_distance": 7.5,
      "tracker_distance": 7.0,
      "logged_activities_distance": 0.5,
      "very_active_minutes": 30,
      "fairly_active_minutes": 55,
      "lightly_active_minutes": 110,
      "sedentary_minutes": 750,
      "calories": 2700,
      "created_at": "2025-04-13T09:00:00Z",
      "updated_at": "2025-04-14T11:00:00Z"
    },
    "message": "Daily activity summary updated successfully."
  }
  ```

#### DELETE /api/v1/users/{user_id}/activities/daily/{date}

Delete a daily activity summary for a specific date.

**Path Parameters**:

- user_id (integer, required): User ID.
- date (string, required): YYYY-MM-DD.

**Response**:

- **204 No Content**: No response body.

---

### **2. Sleep Logs**

Manage sleep log entries.

#### POST /api/v1/users/{user_id}/sleep

Create a new sleep log.

**Path Parameters**:

- user_id (integer, required): User ID.

**Request Body**:

json

```json
{
  "date": "2025-04-14", *// Required, YYYY-MM-DD*
  "start_time": "2025-04-13T22:50:00Z", *// Required, ISO 8601*
  "end_time": "2025-04-14T06:30:00Z", *// Required, ISO 8601*
  "total_minutes_asleep": 430, *// Optional, integer*
  "total_time_in_bed": 460, *// Optional, integer*
  "sleep_efficiency": 93, *// Optional, integer*
  "stages": [ *// Optional*
    { "stage": "deep", "minutes": 85 },
    { "stage": "light", "minutes": 230 },
    { "stage": "rem", "minutes": 95 },
    { "stage": "awake", "minutes": 10 }
  ]
}
```

**Response**:

- **201 Created**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 102,
      "user_id": 123,
      "date": "2025-04-14",
      "start_time": "2025-04-13T22:50:00Z",
      "end_time": "2025-04-14T06:30:00Z",
      "total_minutes_asleep": 430,
      "total_time_in_bed": 460,
      "sleep_efficiency": 93,
      "stages": [
        { "id": 305, "stage": "deep", "minutes": 85, "created_at": "2025-04-14T07:00:00Z" },
        { "id": 306, "stage": "light", "minutes": 230, "created_at": "2025-04-14T07:00:00Z" },
        { "id": 307, "stage": "rem", "minutes": 95, "created_at": "2025-04-14T07:00:00Z" },
        { "id": 308, "stage": "awake", "minutes": 10, "created_at": "2025-04-14T07:00:00Z" }
      ],
      "created_at": "2025-04-14T07:00:00Z",
      "updated_at": "2025-04-14T07:00:00Z"
    },
    "message": "Sleep log created successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/sleep

Retrieve a list of sleep logs.

**Path Parameters**:

- user_id (integer, required): User ID.

**Query Parameters**:

- start_date (string, optional): YYYY-MM-DD.
- end_date (string, optional): YYYY-MM-DD.
- limit (integer, optional).
- offset (integer, optional).

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": [
      {
        "id": 102,
        "user_id": 123,
        "date": "2025-04-14",
        "start_time": "2025-04-13T22:50:00Z",
        "end_time": "2025-04-14T06:30:00Z",
        "total_minutes_asleep": 430,
        "total_time_in_bed": 460,
        "sleep_efficiency": 93,
        "stages": [
          { "id": 305, "stage": "deep", "minutes": 85, "created_at": "2025-04-14T07:00:00Z" }
        ],
        "created_at": "2025-04-14T07:00:00Z",
        "updated_at": "2025-04-14T07:00:00Z"
      }
    ],
    "message": "Sleep logs retrieved successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/sleep/{log_id}

Retrieve a specific sleep log.

**Path Parameters**:

- user_id (integer, required): User ID.
- log_id (integer, required): Sleep log ID.

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 102,
      "user_id": 123,
      "date": "2025-04-14",
      "start_time": "2025-04-13T22:50:00Z",
      "end_time": "2025-04-14T06:30:00Z",
      "total_minutes_asleep": 430,
      "total_time_in_bed": 460,
      "sleep_efficiency": 93,
      "stages": [],
      "created_at": "2025-04-14T07:00:00Z",
      "updated_at": "2025-04-14T07:00:00Z"
    },
    "message": "Sleep log retrieved successfully."
  }
  ```

#### PUT /api/v1/users/{user_id}/sleep/{log_id}

Update a specific sleep log.

**Path Parameters**:

- user_id (integer, required): User ID.
- log_id (integer, required): Sleep log ID.

**Request Body**: (Same as POST /sleep)

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 102,
      "user_id": 123,
      "date": "2025-04-14",
      "start_time": "2025-04-13T22:50:00Z",
      "end_time": "2025-04-14T06:30:00Z",
      "total_minutes_asleep": 430,
      "total_time_in_bed": 460,
      "sleep_efficiency": 93,
      "stages": [],
      "created_at": "2025-04-14T07:00:00Z",
      "updated_at": "2025-04-14T08:00:00Z"
    },
    "message": "Sleep log updated successfully."
  }
  ```

#### DELETE /api/v1/users/{user_id}/sleep/{log_id}

Delete a specific sleep log.

**Path Parameters**:

- user_id (integer, required): User ID.
- log_id (integer, required): Sleep log ID.

**Response**:

- **204 No Content**: No response body.

---

### 3. Heart Rate

Manage heart rate data.

#### POST /api/v1/users/{user_id}/heartrate/logs

Add one or more heart rate log entries.

**Path Parameters**:

- user_id (integer, required): User ID.

**Request Body**:

json

```json
[
  { "datetime": "2025-04-14T08:00:00Z", "value": 65 },
  { "datetime": "2025-04-14T08:00:05Z", "value": 66 },
  { "datetime": "2025-04-14T09:30:15Z", "value": 120, "zone": "Fat Burn" }
]
```

**Response**:

- **201 Created**:

  json

  ```json
  {
    "success": true,
    "data": { "records_processed": 3, "errors": [] },
    "message": "Heart rate logs submitted successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/heartrate/logs

Retrieve heart rate logs within a time range.

**Path Parameters**:

- user_id (integer, required): User ID.

**Query Parameters**:

- start_datetime (string, required): ISO 8601.
- end_datetime (string, required): ISO 8601.
- limit (integer, optional).
- offset (integer, optional).

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": [
      {
        "id": 1001,
        "user_id": 123,
        "datetime": "2025-04-14T08:00:00Z",
        "value": 65,
        "zone": null,
        "created_at": "2025-04-14T08:00:00Z"
      }
    ],
    "message": "Heart rate logs retrieved successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/heartrate/summary

Retrieve daily heart rate summaries.

**Path Parameters**:

- user_id (integer, required): User ID.

**Query Parameters**:

- start_date (string, optional): YYYY-MM-DD.
- end_date (string, optional): YYYY-MM-DD.
- limit (integer, optional).
- offset (integer, optional).

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": [
      {
        "id": 250,
        "user_id": 123,
        "date": "2025-04-13",
        "resting_heart_rate": 62,
        "max_heart_rate": 155,
        "min_heart_rate": 58,
        "avg_heart_rate": 78,
        "out_of_range_minutes": 800,
        "fat_burn_minutes": 90,
        "cardio_minutes": 45,
        "peak_minutes": 15,
        "created_at": "2025-04-13T00:00:00Z",
        "updated_at": "2025-04-13T23:59:59Z"
      }
    ],
    "message": "Heart rate summaries retrieved successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/heartrate/summary/{date}

Retrieve a heart rate summary for a specific date.

**Path Parameters**:

- user_id (integer, required): User ID.
- date (string, required): YYYY-MM-DD.

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 250,
      "user_id": 123,
      "date": "2025-04-13",
      "resting_heart_rate": 62,
      "max_heart_rate": 155,
      "min_heart_rate": 58,
      "avg_heart_rate": 78,
      "out_of_range_minutes": 800,
      "fat_burn_minutes": 90,
      "cardio_minutes": 45,
      "peak_minutes": 15,
      "created_at": "2025-04-13T00:00:00Z",
      "updated_at": "2025-04-13T23:59:59Z"
    },
    "message": "Heart rate summary retrieved successfully."
  }
  ```
---

### **4. Weight Logs**

Manage weight log entries.

#### POST /api/v1/users/{user_id}/weight

Create a new weight log.

**Path Parameters**:

- user_id (integer, required): User ID.

**Request Body**:

json

```json
{
  "date": "2025-04-14", *// Required, YYYY-MM-DD*
  "time": "07:35:00", *// Optional, HH:mm:ss*
  "weight_kg": 75.2, *// Required, float*
  "bmi": 23.2, *// Optional, float*
  "fat_percent": 18.3, *// Optional, float*
  "is_manual_report": true *// Optional, boolean*
}
```

**Response**:

- **201 Created**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 202,
      "user_id": 123,
      "date": "2025-04-14",
      "time": "07:35:00",
      "weight_kg": 75.2,
      "bmi": 23.2,
      "fat_percent": 18.3,
      "is_manual_report": true,
      "created_at": "2025-04-14T07:35:00Z",
      "updated_at": "2025-04-14T07:35:00Z"
    },
    "message": "Weight log created successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/weight

Retrieve a list of weight logs.

**Path Parameters**:

- user_id (integer, required): User ID.

**Query Parameters**:

- start_date (string, optional): YYYY-MM-DD.
- end_date (string, optional): YYYY-MM-DD.
- limit (integer, optional).
- offset (integer, optional).

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": [
      {
        "id": 202,
        "user_id": 123,
        "date": "2025-04-14",
        "time": "07:35:00",
        "weight_kg": 75.2,
        "bmi": 23.2,
        "fat_percent": 18.3,
        "is_manual_report": true,
        "created_at": "2025-04-14T07:35:00Z",
        "updated_at": "2025-04-14T07:35:00Z"
      }
    ],
    "message": "Weight logs retrieved successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/weight/{log_id}

Retrieve a specific weight log.

**Path Parameters**:

- user_id (integer, required): User ID.
- log_id (integer, required): Weight log ID.

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 202,
      "user_id": 123,
      "date": "2025-04-14",
      "time": "07:35:00",
      "weight_kg": 75.2,
      "bmi": 23.2,
      "fat_percent": 18.3,
      "is_manual_report": true,
      "created_at": "2025-04-14T07:35:00Z",
      "updated_at": "2025-04-14T07:35:00Z"
    },
    "message": "Weight log retrieved successfully."
  }
  ```

#### PUT /api/v1/users/{user_id}/weight/{log_id}

Update a specific weight log.

**Path Parameters**:

- user_id (integer, required): User ID.
- log_id (integer, required): Weight log ID.

**Request Body**: (Same as POST /weight)

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 202,
      "user_id": 123,
      "date": "2025-04-14",
      "time": "07:35:00",
      "weight_kg": 75.2,
      "bmi": 23.2,
      "fat_percent": 18.3,
      "is_manual_report": true,
      "created_at": "2025-04-14T07:35:00Z",
      "updated_at": "2025-04-14T08:00:00Z"
    },
    "message": "Weight log updated successfully."
  }
  ```

#### DELETE /api/v1/users/{user_id}/weight/{log_id}

Delete a specific weight log.

**Path Parameters**:

- user_id (integer, required): User ID.
- log_id (integer, required): Weight log ID.

**Response**:

- **204 No Content**: No response body.

---

### **5. Exercise Definitions**

Access standardized exercise definitions.

#### GET /api/v1/exercises/definitions

Retrieve a list of exercise definitions (non-user-specific).

**Query Parameters**:

- limit (integer, optional).
- offset (integer, optional).

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": [
      {
        "id": 1,
        "name": "Running",
        "category": "Cardio",
        "description": null,
        "default_unit": "km"
      },
      {
        "id": 6,
        "name": "Weight Lifting",
        "category": "Strength",
        "description": "General weight training",
        "default_unit": "reps"
      }
    ],
    "message": "Exercise definitions retrieved successfully."
  }
  ```

---

### **6. Exercise Logs**

Manage exercise log entries.

#### POST /api/v1/users/{user_id}/exercises

Create a new exercise log.

**Path Parameters**:

- user_id (integer, required): User ID.

**Request Body**:

json

```json
{
  "date": "2025-04-14", *// Required, YYYY-MM-DD*
  "start_time": "08:00:00", *// Optional, HH:mm:ss*
  "end_time": "09:00:00", *// Optional, HH:mm:ss*
  "exercise_definition_id": 6, *// Required, integer*
  "duration_minutes": 60, *// Required, integer*
  "calories_burned": 400, *// Optional, integer*
  "avg_heart_rate": 130, *// Optional, integer*
  "max_heart_rate": 150, *// Optional, integer*
  "distance_km": null, *// Optional, float*
  "notes": "Upper body session.", *// Optional, string*
  "routine_id": 15 *// Optional, integer*
}
```

**Response**:

- **201 Created**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 302,
      "user_id": 123,
      "date": "2025-04-14",
      "start_time": "08:00:00",
      "end_time": "09:00:00",
      "exercise_definition_id": 6,
      "duration_minutes": 60,
      "calories_burned": 400,
      "avg_heart_rate": 130,
      "max_heart_rate": 150,
      "distance_km": null,
      "notes": "Upper body session.",
      "routine_id": 15,
      "created_at": "2025-04-14T09:00:00Z",
      "updated_at": "2025-04-14T09:00:00Z"
    },
    "message": "Exercise log created successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/exercises

Retrieve a list of exercise logs.

**Path Parameters**:

- user_id (integer, required): User ID.

**Query Parameters**:

- start_date (string, optional): YYYY-MM-DD.
- end_date (string, optional): YYYY-MM-DD.
- exercise_definition_id (integer, optional).
- routine_id (integer, optional).
- limit (integer, optional).
- offset (integer, optional).

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": [
      {
        "id": 302,
        "user_id": 123,
        "date": "2025-04-14",
        "start_time": "08:00:00",
        "end_time": "09:00:00",
        "exercise_definition_id": 6,
        "duration_minutes": 60,
        "calories_burned": 400,
        "avg_heart_rate": 130,
        "max_heart_rate": 150,
        "distance_km": null,
        "notes": "Upper body session.",
        "routine_id": 15,
        "created_at": "2025-04-14T09:00:00Z",
        "updated_at": "2025-04-14T09:00:00Z"
      }
    ],
    "message": "Exercise logs retrieved successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/exercises/{log_id}

Retrieve a specific exercise log.

**Path Parameters**:

- user_id (integer, required): User ID.
- log_id (integer, required): Exercise log ID.

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 302,
      "user_id": 123,
      "date": "2025-04-14",
      "start_time": "08:00:00",
      "end_time": "09:00:00",
      "exercise_definition_id": 6,
      "duration_minutes": 60,
      "calories_burned": 400,
      "avg_heart_rate": 130,
      "max_heart_rate": 150,
      "distance_km": null,
      "notes": "Upper body session.",
      "routine_id": 15,
      "created_at": "2025-04-14T09:00:00Z",
      "updated_at": "2025-04-14T09:00:00Z"
    },
    "message": "Exercise log retrieved successfully."
  }
  ```

#### PUT /api/v1/users/{user_id}/exercises/{log_id}

Update a specific exercise log.

**Path Parameters**:

- user_id (integer, required): User ID.
- log_id (integer, required): Exercise log ID.

**Request Body**: (Same as POST /exercises)

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 302,
      "user_id": 123,
      "date": "2025-04-14",
      "start_time": "08:00:00",
      "end_time": "09:00:00",
      "exercise_definition_id": 6,
      "duration_minutes": 60,
      "calories_burned": 400,
      "avg_heart_rate": 130,
      "max_heart_rate": 150,
      "distance_km": null,
      "notes": "Upper body session.",
      "routine_id": 15,
      "created_at": "2025-04-14T09:00:00Z",
      "updated_at": "2025-04-14T10:00:00Z"
    },
    "message": "Exercise log updated successfully."
  }
  ```

#### DELETE /api/v1/users/{user_id}/exercises/{log_id}

Delete a specific exercise log.

**Path Parameters**:

- user_id (integer, required): User ID.
- log_id (integer, required): Exercise log ID.

**Response**:

- **204 No Content**: No response body.

---

## 7. Routines

Manage workout routines.

#### POST /api/v1/users/{user_id}/routines

Create a new routine with exercises.

**Path Parameters**:

- user_id (integer, required): User ID.

**Request Body**:

json

```json
{
  "name": "Full Body Workout", *// Required, string*
  "description": "Basic full body routine.", *// Optional, string*
  "exercises": [ *// Required, array*
    {
      "exercise_definition_id": 8, *// Required, integer*
      "sets": 3, *// Optional, integer*
      "reps": 10, *// Optional, integer*
      "weight_kg": null, *// Optional, float*
      "duration_minutes": null, *// Optional, integer*
      "distance_km": null, *// Optional, float*
      "order_in_routine": 1, *// Required, integer*
      "notes": "Focus on form." *// Optional, string*
    },
    {
      "exercise_definition_id": 7,
      "sets": 3,
      "reps": 8,
      "weight_kg": 60,
      "order_in_routine": 2,
      "notes": null
    }
  ]
}
```

**Response**:

- **201 Created**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 16,
      "user_id": 123,
      "name": "Full Body Workout",
      "description": "Basic full body routine.",
      "exercises": [
        {
          "id": 45,
          "routine_id": 16,
          "exercise_definition_id": 8,
          "sets": 3,
          "reps": 10,
          "weight_kg": null,
          "duration_minutes": null,
          "distance_km": null,
          "order_in_routine": 1,
          "notes": "Focus on form.",
          "created_at": "2025-04-14T10:00:00Z"
        },
        {
          "id": 46,
          "routine_id": 16,
          "exercise_definition_id": 7,
          "sets": 3,
          "reps": 8,
          "weight_kg": 60,
          "duration_minutes": null,
          "distance_km": null,
          "order_in_routine": 2,
          "notes": null,
          "created_at": "2025-04-14T10:00:00Z"
        }
      ],
      "created_at": "2025-04-14T10:00:00Z",
      "updated_at": "2025-04-14T10:00:00Z"
    },
    "message": "Routine created successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/routines

Retrieve a list of routines.

**Path Parameters**:

- user_id (integer, required): User ID.

**Query Parameters**:

- limit (integer, optional).
- offset (integer, optional).

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": [
      {
        "id": 16,
        "user_id": 123,
        "name": "Full Body Workout",
        "description": "Basic full body routine.",
        "created_at": "2025-04-14T10:00:00Z",
        "updated_at": "2025-04-14T10:00:00Z",
        "exercise_count": 2
      }
    ],
    "message": "Routines retrieved successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/routines/{routine_id}

Retrieve a specific routine with exercise details.

**Path Parameters**:

- user_id (integer, required): User ID.
- routine_id (integer, required): Routine ID.

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 16,
      "user_id": 123,
      "name": "Full Body Workout",
      "description": "Basic full body routine.",
      "exercises": [
        {
          "id": 45,
          "routine_id": 16,
          "exercise_definition_id": 8,
          "sets": 3,
          "reps": 10,
          "weight_kg": null,
          "duration_minutes": null,
          "distance_km": null,
          "order_in_routine": 1,
          "notes": "Focus on form.",
          "created_at": "2025-04-14T10:00:00Z"
        }
      ],
      "created_at": "2025-04-14T10:00:00Z",
      "updated_at": "2025-04-14T10:00:00Z"
    },
    "message": "Routine retrieved successfully."
  }
  ```

#### PUT /api/v1/users/{user_id}/routines/{routine_id}

Update a specific routine.

**Path Parameters**:

- user_id (integer, required): User ID.
- routine_id (integer, required): Routine ID.

**Request Body**: (Same as POST /routines)

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 16,
      "user_id": 123,
      "name": "Full Body Workout",
      "description": "Basic full body routine.",
      "exercises": [],
      "created_at": "2025-04-14T10:00:00Z",
      "updated_at": "2025-04-14T11:00:00Z"
    },
    "message": "Routine updated successfully."
  }
  ```

#### DELETE /api/v1/users/{user_id}/routines/{routine_id}

Delete a specific routine.

**Path Parameters**:

- user_id (integer, required): User ID.
- routine_id (integer, required): Routine ID.

**Response**:

- **204 No Content**: No response body.

---

### **8. Goals**

Manage user goals.

#### POST /api/v1/users/{user_id}/goals

Create a new goal.

**Path Parameters**:

- user_id (integer, required): User ID.

**Request Body**:

json

```json
{
  "name": "Run a 5K", *// Optional, string*
  "goal_type": "exercise_distance", *// Required, string*
  "target_value": 5.0, *// Required, float*
  "target_unit": "km", *// Required, string*
  "start_value": 0.0, *// Optional, float*
  "start_date": "2025-05-01", *// Required, YYYY-MM-DD*
  "target_date": "2025-08-01" *// Optional, YYYY-MM-DD*
}
```

**Response**:

- **201 Created**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 402,
      "user_id": 123,
      "name": "Run a 5K",
      "goal_type": "exercise_distance",
      "target_value": 5.0,
      "target_unit": "km",
      "start_value": 0.0,
      "current_value": 0.0,
      "start_date": "2025-05-01",
      "target_date": "2025-08-01",
      "is_completed": false,
      "completion_date": null,
      "created_at": "2025-04-14T12:00:00Z",
      "updated_at": "2025-04-14T12:00:00Z"
    },
    "message": "Goal created successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/goals

Retrieve a list of goals.

**Path Parameters**:

- user_id (integer, required): User ID.

**Query Parameters**:

- status (string, optional): active, completed, all.
- limit (integer, optional).
- offset (integer, optional).

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": [
      {
        "id": 402,
        "user_id": 123,
        "name": "Run a 5K",
        "goal_type": "exercise_distance",
        "target_value": 5.0,
        "target_unit": "km",
        "start_value": 0.0,
        "current_value": 0.0,
        "start_date": "2025-05-01",
        "target_date": "2025-08-01",
        "is_completed": false,
        "completion_date": null,
        "created_at": "2025-04-14T12:00:00Z",
        "updated_at": "2025-04-14T12:00:00Z"
      }
    ],
    "message": "Goals retrieved successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/goals/{goal_id}

Retrieve a specific goal.

**Path Parameters**:

- user_id (integer, required): User ID.
- goal_id (integer, required): Goal ID.

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 402,
      "user_id": 123,
      "name": "Run a 5K",
      "goal_type": "exercise_distance",
      "target_value": 5.0,
      "target_unit": "km",
      "start_value": 0.0,
      "current_value": 0.0,
      "start_date": "2025-05-01",
      "target_date": "2025-08-01",
      "is_completed": false,
      "completion_date": null,
      "created_at": "2025-04-14T12:00:00Z",
      "updated_at": "2025-04-14T12:00:00Z"
    },
    "message": "Goal retrieved successfully."
  }
  ```

#### PUT /api/v1/users/{user_id}/goals/{goal_id}

Update a specific goal.

**Path Parameters**:

- user_id (integer, required): User ID.
- goal_id (integer, required): Goal ID.

**Request Body**:

json

```json
{
  "name": "Run a 5K Race", *// Optional, string*
  "target_date": "2025-07-30", *// Optional, YYYY-MM-DD*
  "current_value": 2.5 *// Optional, float*
}
```

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 402,
      "user_id": 123,
      "name": "Run a 5K Race",
      "goal_type": "exercise_distance",
      "target_value Quelle: 5.0,
      "target_unit": "km",
      "start_value": 0.0,
      "current_value": 2.5,
      "start_date": "2025-05-01",
      "target_date": "2025-07-30",
      "is_completed": false,
      "completion_date": null,
      "created_at": "2025-04-14T12:00:00Z",
      "updated_at": "2025-04-14T13:00:00Z"
    },
    "message": "Goal updated successfully."
  }
  ```

#### DELETE /api/v1/users/{user_id}/goals/{goal_id}

Delete a specific goal.

**Path Parameters**:

- user_id (integer, required): User ID.
- goal_id (integer, required): Goal ID.

**Response**:

- **204 No Content**: No response body.

---

### **9. Achievements**

Manage achievements.

#### GET /api/v1/achievements

Retrieve a list of all achievement definitions.

**Query Parameters**:

- limit (integer, optional).
- offset (integer, optional).

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": [
      {
        "id": 1,
        "name": "Daily Steps Bronze",
        "description": "Walk 5,000 steps in a single day",
        "badge_icon": "steps_bronze.png",
        "achievement_type": "steps",
        "threshold_value": 5000.0,
        "threshold_unit": "steps",
        "created_at": "2025-04-14T00:00:00Z"
      }
    ],
    "message": "Achievement definitions retrieved successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/achievements

Retrieve a list of achievements earned by a user.

**Path Parameters**:

- user_id (integer, required): User ID.

**Query Parameters**:

- limit (integer, optional).
- offset (integer, optional).

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": [
      {
        "user_achievement_id": 501,
        "achievement_id": 1,
        "name": "Daily Steps Bronze",
        "description": "Walk 5,000 steps in a single day",
        "badge_icon": "steps_bronze.png",
        "achievement_type": "steps",
        "threshold_value": 5000.0,
        "threshold_unit": "steps",
        "date_achieved": "2025-04-12T18:30:00Z"
      }
    ],
    "message": "User achievements retrieved successfully."
  }
  ```

---

### **10. Data Imports**

Manage data import tasks.

#### POST /api/v1/users/{user_id}/imports

Start a new data import task.

**Path Parameters**:

- user_id (integer, required): User ID.

**Request Body** (multipart/form-data):

- import_type (string, required): e.g., csv, fitbit_api.
- source (string, optional): e.g., filename.
- file (file, required for csv imports).
- api_credentials (object, required for API imports).

**Response**:

- **202 Accepted**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 601,
      "user_id": 123,
      "import_type": "csv",
      "source": "my_fitbit_data.csv",
      "record_count": 0,
      "status": "pending",
      "error_message": null,
      "import_date": "2025-04-14T10:00:00Z",
      "created_at": "2025-04-14T10:00:00Z"
    },
    "message": "Data import task accepted and queued for processing."
  }
  ```

#### GET /api/v1/users/{user_id}/imports

Retrieve a list of data import history.

**Path Parameters**:

- user_id (integer, required): User ID.

**Query Parameters**:

- limit (integer, optional).
- offset (integer, optional).

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": [
      {
        "id": 601,
        "user_id": 123,
        "import_type": "csv",
        "source": "my_fitbit_data.csv",
        "record_count": 1500,
        "status": "completed",
        "error_message": null,
        "import_date": "2025-04-14T10:00:00Z",
        "created_at": "2025-04-14T10:00:00Z"
      }
    ],
    "message": "Data import history retrieved successfully."
  }
  ```

#### GET /api/v1/users/{user_id}/imports/{import_id}

Retrieve details of a specific data import task.

**Path Parameters**:

- user_id (integer, required): User ID.
- import_id (integer, required): Import task ID.

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 601,
      "user_id": 123,
      "import_type": "csv",
      "source": "my_fitbit_data.csv",
      "record_count": 1500,
      "status": "completed",
      "error_message": null,
      "import_date": "2025-04-14T10:00:00Z",
      "created_at": "2025-04-14T10:00:00Z"
    },
    "message": "Data import status retrieved successfully."
  }
  ```
---

### **11. Recommendations**

Manage health recommendations.

#### GET /api/v1/users/{user_id}/recommendations

Retrieve a list of recommendations.

**Path Parameters**:

- user_id (integer, required): User ID.

**Query Parameters**:

- status (string, optional): new, viewed, actioned, all.
- limit (integer, optional).
- offset (integer, optional).

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": [
      {
        "id": 701,
        "user_id": 123,
        "recommendation_text": "Your average sleep duration was low last week. Try aiming for 7-8 hours tonight.",
        "recommendation_type": "sleep",
        "related_item_type": "sleep_log_summary",
        "related_item_id": 85,
        "created_at": "2025-04-14T09:00:00Z",
        "is_viewed": false,
        "viewed_at": null,
        "is_actioned": false,
        "actioned_at": null,
        "priority": "medium"
      }
    ],
    "message": "Recommendations retrieved successfully."
  }
  ```

#### PUT /api/v1/users/{user_id}/recommendations/{recommendation_id}

Update the status of a recommendation.

**Path Parameters**:

- user_id (integer, required): User ID.
- recommendation_id (integer, required): Recommendation ID.

**Request Body**:

json

```json
{
  "is_viewed": true, *// Optional, boolean*
  "is_actioned": true *// Optional, boolean*
}
```

**Response**:

- **200 OK**:

  json

  ```json
  {
    "success": true,
    "data": {
      "id": 701,
      "user_id": 123,
      "recommendation_text": "Your average sleep duration was low last week. Try aiming for 7-8 hours tonight.",
      "recommendation_type": "sleep",
      "related_item_type": "sleep_log_summary",
      "related_item_id": 85,
      "created_at": "2025-04-14T09:00:00Z",
      "is_viewed": true,
      "viewed_at": "2025-04-14T11:30:00Z",
      "is_actioned": true,
      "actioned_at": "2025-04-14T11:30:00Z",
      "priority": "medium"
    },
    "message": "Recommendation status updated successfully."
  }
  ```

------

### **12. Error Responses (General)**

Common error responses for all endpoints (included sparingly per your preference):

- **400 Bad Request** (Validation error):

  json

  ```json
  {
    "success": false,
    "data": { "field": "Error message" },
    "message": "Invalid input data.",
    "error": "VALIDATION_ERROR"
  }
  ```



- **404 Not Found** (Resource not found):

  json

  ```json
  {
    "success": false,
    "data": null,
    "message": "Resource not found.",
    "error": "NOT_FOUND"
  } 		
  ```
---

  
