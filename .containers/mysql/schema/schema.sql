CREATE TABLE
    IF NOT EXISTS `detail_log` (
        `id` bigint NOT NULL AUTO_INCREMENT,
        `script_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        `script_run_time` datetime NOT NULL,
        `message` text DEFAULT NULL,
        `level` enum(
            'CRITICAL',
            'INFO',
            'DEBUG',
            'ERROR',
            'WARNING',
            'NOTSET'
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        `process_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        PRIMARY KEY (`id`),
        KEY `script_name` (`script_name`),
        KEY `script_run_time` (`script_run_time`),
        KEY `level` (`level`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    IF NOT EXISTS `job_log` (
        `id` bigint NOT NULL AUTO_INCREMENT,
        `script_end_time` datetime NOT NULL,
        `script_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        `script_start_time` datetime NOT NULL,
        `job_summary_data` mediumtext DEFAULT NULL,
        `job_duration` double not null,
        `level` enum(
            'CRITICAL',
            'INFO',
            'DEBUG',
            'ERROR',
            'WARNING',
            'NOTSET'
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        `process_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        PRIMARY KEY (`id`),
        KEY `script_end_time` (`script_end_time`),
        KEY `script_name` (`script_name`),
        KEY `script_start_time` (`script_start_time`),
        KEY `level` (`level`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    IF NOT EXISTS `test_detail_log` (
        `id` bigint NOT NULL AUTO_INCREMENT,
        `script_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        `script_run_time` datetime NOT NULL,
        `message` text DEFAULT NULL,
        `level` enum(
            'CRITICAL',
            'INFO',
            'DEBUG',
            'ERROR',
            'WARNING',
            'NOTSET'
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        `process_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        PRIMARY KEY (`id`),
        KEY `script_name` (`script_name`),
        KEY `script_run_time` (`script_run_time`),
        KEY `level` (`level`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    IF NOT EXISTS `test_job_log` (
        `id` bigint NOT NULL AUTO_INCREMENT,
        `script_end_time` datetime NOT NULL,
        `script_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        `script_start_time` datetime NOT NULL,
        `job_summary_data` mediumtext DEFAULT NULL,
        `job_duration` double not null,
        `level` enum(
            'CRITICAL',
            'INFO',
            'DEBUG',
            'ERROR',
            'WARNING',
            'NOTSET'
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        `process_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        PRIMARY KEY (`id`),
        KEY `script_end_time` (`script_end_time`),
        KEY `script_name` (`script_name`),
        KEY `script_start_time` (`script_start_time`),
        KEY `level` (`level`)
    ) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE OR REPLACE VIEW V_RCC_DETAIL_LOG AS 
	SELECT
	    id,
	    script_run_time as log_date,
	    script_name,
	    script_run_time,
	    'message',
	    'level'
	FROM
DETAIL_LOG; 

CREATE OR REPLACE VIEW V_RCC_JOB_LOG AS 
	SELECT
	    id,
	    script_end_time as log_date,
	    script_name,
	    script_start_time as script_run_time,
	    job_summary_data,
	    job_duration,
	    'level'
	FROM
JOB_LOG; 