# 补充三：数据库正式建表 SQL（补充 PRD §29）

## 1. 通用约定

- 字符集：UTF-8
- 引擎：PostgreSQL 14+
- 时间字段统一使用 `TIMESTAMP WITH TIME ZONE`
- ID 字段统一使用 `VARCHAR(64)`
- 所有表包含 `created_time` 和 `updated_time`
- 状态字段使用 VARCHAR，不使用枚举类型（便于扩展）

## 2. 建表 SQL

### 2.1 对象主表

```sql
CREATE TABLE object_info (
    object_id       VARCHAR(64)     PRIMARY KEY,
    object_name     VARCHAR(128)    NOT NULL,
    object_type     VARCHAR(32)     NOT NULL CHECK (object_type IN ('bridge', 'tunnel')),
    location_desc   VARCHAR(255),
    status          VARCHAR(32)     NOT NULL DEFAULT 'active',
    created_time    TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_time    TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE object_info IS '桥梁和隧道对象主数据';
COMMENT ON COLUMN object_info.object_id IS '对象唯一标识';
COMMENT ON COLUMN object_info.object_name IS '对象名称';
COMMENT ON COLUMN object_info.object_type IS '对象类型：bridge-桥梁, tunnel-隧道';
COMMENT ON COLUMN object_info.location_desc IS '位置描述';
COMMENT ON COLUMN object_info.status IS '状态：active-启用, inactive-停用';

CREATE INDEX idx_object_info_type ON object_info(object_type);
CREATE INDEX idx_object_info_status ON object_info(status);
```

### 2.2 视频主表

```sql
CREATE TABLE video_info (
    video_id            VARCHAR(64)     PRIMARY KEY,
    object_id           VARCHAR(64)     NOT NULL,
    video_name          VARCHAR(255)    NOT NULL,
    file_url            VARCHAR(500)    NOT NULL,
    capture_time        TIMESTAMPTZ,
    duration_seconds    INT,
    resolution          VARCHAR(64),
    scene_type          VARCHAR(32)     CHECK (scene_type IN ('day', 'night', 'rain_fog')),
    preprocess_status   VARCHAR(32)     NOT NULL DEFAULT 'pending',
    created_time        TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_time        TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_video_object FOREIGN KEY (object_id) REFERENCES object_info(object_id)
);

COMMENT ON TABLE video_info IS '视频文件与元数据';
COMMENT ON COLUMN video_info.preprocess_status IS '预处理状态：pending-待处理, processing-处理中, completed-已完成, failed-失败';

CREATE INDEX idx_video_info_object ON video_info(object_id);
CREATE INDEX idx_video_info_capture ON video_info(capture_time);
CREATE INDEX idx_video_info_scene ON video_info(scene_type);
CREATE INDEX idx_video_info_preprocess ON video_info(preprocess_status);
```

### 2.3 事件表

```sql
CREATE TABLE event_record (
    event_id        VARCHAR(64)     PRIMARY KEY,
    object_id       VARCHAR(64)     NOT NULL,
    video_id        VARCHAR(64)     NOT NULL,
    event_type      VARCHAR(64)     NOT NULL,
    risk_level      VARCHAR(32)     NOT NULL DEFAULT 'low' CHECK (risk_level IN ('low', 'medium', 'high')),
    scene_type      VARCHAR(32)     CHECK (scene_type IN ('day', 'night', 'rain_fog')),
    event_time      TIMESTAMPTZ     NOT NULL,
    start_second    INT             NOT NULL,
    end_second      INT             NOT NULL,
    thumbnail_url   VARCHAR(500),
    clip_url        VARCHAR(500),
    result_desc     TEXT,
    review_status   VARCHAR(32)     NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending', 'reviewed')),
    review_remark   TEXT,
    created_time    TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_time    TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_event_object FOREIGN KEY (object_id) REFERENCES object_info(object_id),
    CONSTRAINT fk_event_video FOREIGN KEY (video_id) REFERENCES video_info(video_id)
);

COMMENT ON TABLE event_record IS '识别事件记录';
COMMENT ON COLUMN event_record.event_type IS '事件类型：collapse/deformation/congestion/fire/ship_collision/tunnel_anomaly';
COMMENT ON COLUMN event_record.start_second IS '事件在视频中的开始秒数';
COMMENT ON COLUMN event_record.end_second IS '事件在视频中的结束秒数';

CREATE INDEX idx_event_record_object ON event_record(object_id);
CREATE INDEX idx_event_record_video ON event_record(video_id);
CREATE INDEX idx_event_record_time ON event_record(event_time);
CREATE INDEX idx_event_record_type ON event_record(event_type);
CREATE INDEX idx_event_record_risk ON event_record(risk_level);
CREATE INDEX idx_event_record_review ON event_record(review_status);
-- 组合索引：支持事件中心多条件查询
CREATE INDEX idx_event_record_query ON event_record(object_id, event_type, risk_level, event_time);
```

### 2.4 模型版本表

```sql
CREATE TABLE model_version (
    model_id        VARCHAR(64)     PRIMARY KEY,
    model_name      VARCHAR(128)    NOT NULL,
    model_type      VARCHAR(64)     NOT NULL,
    model_version   VARCHAR(64)     NOT NULL,
    file_url        VARCHAR(500),
    status          VARCHAR(32)     NOT NULL DEFAULT 'inactive' CHECK (status IN ('active', 'inactive', 'deprecated')),
    publish_time    TIMESTAMPTZ,
    remark          VARCHAR(255),
    created_time    TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_time    TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE model_version IS '模型版本管理';
COMMENT ON COLUMN model_version.model_type IS '模型类型：bridge-普通桥梁, ship_collision-船撞, tunnel-隧道';

CREATE INDEX idx_model_version_type ON model_version(model_type);
CREATE INDEX idx_model_version_status ON model_version(status);
```

### 2.5 推理任务表

```sql
CREATE TABLE inference_task (
    task_id         VARCHAR(64)     PRIMARY KEY,
    video_id        VARCHAR(64)     NOT NULL,
    model_id        VARCHAR(64)     NOT NULL,
    task_name       VARCHAR(255),
    task_status     VARCHAR(32)     NOT NULL DEFAULT 'queued' CHECK (task_status IN ('queued', 'running', 'success', 'failed')),
    start_time      TIMESTAMPTZ,
    end_time        TIMESTAMPTZ,
    result_summary  TEXT,
    error_message   TEXT,
    created_time    TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_task_video FOREIGN KEY (video_id) REFERENCES video_info(video_id),
    CONSTRAINT fk_task_model FOREIGN KEY (model_id) REFERENCES model_version(model_id)
);

COMMENT ON TABLE inference_task IS '推理任务记录';

CREATE INDEX idx_inference_task_video ON inference_task(video_id);
CREATE INDEX idx_inference_task_model ON inference_task(model_id);
CREATE INDEX idx_inference_task_status ON inference_task(task_status);
CREATE INDEX idx_inference_task_created ON inference_task(created_time);
```

### 2.6 监测数据表

```sql
CREATE TABLE monitoring_data (
    data_id         BIGSERIAL       PRIMARY KEY,
    object_id       VARCHAR(64)     NOT NULL,
    data_type       VARCHAR(64)     NOT NULL,
    data_time       TIMESTAMPTZ     NOT NULL,
    data_value      DECIMAL(18,4)   NOT NULL,
    ext_json        JSONB,
    created_time    TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_monitoring_object FOREIGN KEY (object_id) REFERENCES object_info(object_id)
);

COMMENT ON TABLE monitoring_data IS '结构与环境监测数据';
COMMENT ON COLUMN monitoring_data.data_type IS '数据类型：displacement/vibration/strain/water_level/ais/temperature/smoke/gas';
COMMENT ON COLUMN monitoring_data.ext_json IS '扩展字段，JSON格式存储额外属性';

CREATE INDEX idx_monitoring_data_object ON monitoring_data(object_id);
CREATE INDEX idx_monitoring_data_type ON monitoring_data(data_type);
CREATE INDEX idx_monitoring_data_time ON monitoring_data(data_time);
-- 组合索引：支持按对象+类型+时间范围查询
CREATE INDEX idx_monitoring_data_query ON monitoring_data(object_id, data_type, data_time);
```

### 2.7 融合结果表

```sql
CREATE TABLE fusion_result (
    fusion_id           VARCHAR(64)     PRIMARY KEY,
    object_id           VARCHAR(64)     NOT NULL,
    related_event_id    VARCHAR(64),
    fusion_type         VARCHAR(64)     NOT NULL CHECK (fusion_type IN ('ship_collision', 'tunnel')),
    score               DECIMAL(8,2)    NOT NULL,
    risk_level          VARCHAR(32)     NOT NULL CHECK (risk_level IN ('low', 'medium', 'high')),
    rule_desc           TEXT,
    fusion_time         TIMESTAMPTZ     NOT NULL,
    created_time        TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_fusion_object FOREIGN KEY (object_id) REFERENCES object_info(object_id),
    CONSTRAINT fk_fusion_event FOREIGN KEY (related_event_id) REFERENCES event_record(event_id)
);

COMMENT ON TABLE fusion_result IS '融合预警结果';

CREATE INDEX idx_fusion_result_object ON fusion_result(object_id);
CREATE INDEX idx_fusion_result_type ON fusion_result(fusion_type);
CREATE INDEX idx_fusion_result_time ON fusion_result(fusion_time);
CREATE INDEX idx_fusion_result_risk ON fusion_result(risk_level);
```

### 2.8 系统日志表

```sql
CREATE TABLE system_log (
    log_id          BIGSERIAL       PRIMARY KEY,
    log_type        VARCHAR(64)     NOT NULL,
    related_id      VARCHAR(64),
    log_level       VARCHAR(16)     NOT NULL DEFAULT 'info' CHECK (log_level IN ('info', 'warn', 'error')),
    log_content     TEXT            NOT NULL,
    created_time    TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE system_log IS '系统日志';
COMMENT ON COLUMN system_log.log_type IS '日志类型：task/error/system/inference';

CREATE INDEX idx_system_log_type ON system_log(log_type);
CREATE INDEX idx_system_log_level ON system_log(log_level);
CREATE INDEX idx_system_log_created ON system_log(created_time);
CREATE INDEX idx_system_log_related ON system_log(related_id);
```

## 3. 更新触发器（自动更新 updated_time）

```sql
CREATE OR REPLACE FUNCTION update_updated_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_time = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 为所有包含 updated_time 的表创建触发器
CREATE TRIGGER trg_object_info_updated BEFORE UPDATE ON object_info
    FOR EACH ROW EXECUTE FUNCTION update_updated_time();

CREATE TRIGGER trg_video_info_updated BEFORE UPDATE ON video_info
    FOR EACH ROW EXECUTE FUNCTION update_updated_time();

CREATE TRIGGER trg_event_record_updated BEFORE UPDATE ON event_record
    FOR EACH ROW EXECUTE FUNCTION update_updated_time();

CREATE TRIGGER trg_model_version_updated BEFORE UPDATE ON model_version
    FOR EACH ROW EXECUTE FUNCTION update_updated_time();
```

## 4. 初始化数据

```sql
-- 初始化字典数据（如有字典表可在此插入）
-- 初始化默认模型记录
INSERT INTO model_version (model_id, model_name, model_type, model_version, status, publish_time, remark)
VALUES
    ('MDL-BRIDGE-V1.0', '普通桥梁风险识别模型V1.0', 'bridge', 'V1.0', 'active', NOW(), '一期基线模型'),
    ('MDL-SHIP-V0.1', '船撞融合预警原型V0.1', 'ship_collision', 'V0.1', 'inactive', NULL, '原型验证模型'),
    ('MDL-TUNNEL-V0.1', '隧道融合预警原型V0.1', 'tunnel', 'V0.1', 'inactive', NULL, '原型验证模型');
```
