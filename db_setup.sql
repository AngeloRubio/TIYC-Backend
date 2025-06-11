CREATE DATABASE IF NOT EXISTS santa_fe CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE santa_fe;

-- Tabla de profesores/usuarios
CREATE TABLE IF NOT EXISTS teachers (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    school VARCHAR(255),
    grade VARCHAR(100),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de cuentos
CREATE TABLE IF NOT EXISTS stories (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    context TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    pedagogical_approach VARCHAR(20) NOT NULL DEFAULT 'traditional',
    teacher_id VARCHAR(36),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL
);

-- Tabla de escenarios
CREATE TABLE IF NOT EXISTS scenarios (
    id VARCHAR(36) PRIMARY KEY,
    story_id VARCHAR(36) NOT NULL,
    description TEXT NOT NULL,
    sequence_number INT NOT NULL,
    prompt_for_image TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

-- Tabla de imágenes
CREATE TABLE IF NOT EXISTS images (
    id VARCHAR(36) PRIMARY KEY,
    scenario_id VARCHAR(36) NOT NULL,
    prompt TEXT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES scenarios(id) ON DELETE CASCADE
);

-- Índices para rendimiento
CREATE INDEX IF NOT EXISTS idx_stories_teacher_id ON stories(teacher_id);
CREATE INDEX IF NOT EXISTS idx_stories_pedagogical ON stories(pedagogical_approach);
CREATE INDEX IF NOT EXISTS idx_scenarios_story_id ON scenarios(story_id);
CREATE INDEX IF NOT EXISTS idx_images_scenario_id ON images(scenario_id);
CREATE INDEX IF NOT EXISTS idx_stories_created_at ON stories(created_at);
CREATE INDEX IF NOT EXISTS idx_scenarios_sequence_number ON scenarios(sequence_number);

-- Usuario de prueba
INSERT INTO teachers (id, username, email, password_hash, school, grade)
SELECT 
    'e7c2359a-8b7a-4880-8c6f-28e349f3e3a0', 
    'profesor_test', 
    'profesor@test.com', 
    '$2b$12$LZk/d7VkDVpuWE1K.qVyVe3KeI0QFRwmvZrJZkrUy9xwlKxdCqkXG',
    'Escuela Primaria Santa Fe',
    'Primaria'
FROM dual
WHERE NOT EXISTS (SELECT 1 FROM teachers LIMIT 1);

-- Procedimientos almacenados
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS CleanOrphanedImages()
BEGIN
    DELETE i FROM images i
    LEFT JOIN scenarios s ON i.scenario_id = s.id
    WHERE s.id IS NULL;
    
    SELECT CONCAT('Limpieza completada. Filas afectadas: ', ROW_COUNT()) AS result;
END //

CREATE PROCEDURE IF NOT EXISTS GetCompleteStory(IN p_story_id VARCHAR(36))
BEGIN
    SELECT * FROM stories WHERE id = p_story_id;
    
    SELECT 
        s.*, 
        i.id as image_id, 
        i.prompt as image_prompt, 
        i.image_url
    FROM scenarios s
    LEFT JOIN images i ON s.id = i.scenario_id
    WHERE s.story_id = p_story_id
    ORDER BY s.sequence_number;
END //
DELIMITER ;