
-- Cria a tabela guild_settings
CREATE TABLE IF NOT EXISTS guild_settings (
    guild_id BIGINT PRIMARY KEY,
    enabled_cogs TEXT[] NOT NULL DEFAULT '{}',
    language TEXT NOT NULL DEFAULT 'en_us',
    loaded_cogs TEXT[] NOT NULL DEFAULT '{}',
    welcome_channel_id BIGINT,
    welcome_mode TEXT, -- "disabled", "fixed", "random"
    selected_welcome_message_id BIGINT, -- usado quando modo de mensagem de boas vindas = fixed
    goodbye_channel_id BIGINT,
    goodbye_mode TEXT, -- "disabled", "fixed", "random"
    selected_goodbye_message_id BIGINT, -- usado quando modo de mensagem de despedida = fixed
    rules_channel_id BIGINT,
    rules_message TEXT,
    rules_required BOOLEAN DEFAULT FALSE,
    intro_channel_id BIGINT,
    intro_template TEXT,
    intro_questions JSONB, -- Lista de perguntas e cargos associados
    custom_roles_enabled BOOLEAN DEFAULT FALSE
);

-- Cria a tabela welcome_messages
CREATE TABLE IF NOT EXISTS welcome_messages (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT,
    title TEXT,
    description TEXT,
    title_url TEXT,
    color INTEGER,
    author_name TEXT,
    author_url TEXT,
    author_icon_url TEXT,
    fields JSONB,
    image_url TEXT,
    thumbnail_url TEXT,
    footer_text TEXT,
    footer_icon_url TEXT,
    timestamp TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (guild_id) REFERENCES guild_settings(guild_id)
);

-- Cria a tabela goodbye_messages
CREATE TABLE IF NOT EXISTS goodbye_messages (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT,
    title TEXT,
    description TEXT,
    title_url TEXT,
    color INTEGER,
    author_name TEXT,
    author_url TEXT,
    author_icon_url TEXT,
    fields JSONB,
    image_url TEXT,
    thumbnail_url TEXT,
    footer_text TEXT,
    footer_icon_url TEXT,
    timestamp TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (guild_id) REFERENCES guild_settings(guild_id)
);

-- Cria a tabela intro_templates
CREATE TABLE IF NOT EXISTS intro_templates (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT UNIQUE,
    title TEXT,
    description TEXT,
    title_url TEXT,
    color INTEGER,
    author_name TEXT,
    author_url TEXT,
    author_icon_url TEXT,
    fields JSONB,
    image_url TEXT,
    thumbnail_url TEXT,
    footer_text TEXT,
    footer_icon_url TEXT,
    timestamp TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (guild_id) REFERENCES guild_settings(guild_id)
);

-- Cria a tabela user_intros
CREATE TABLE IF NOT EXISTS user_intros (
    user_id BIGINT PRIMARY KEY,
    guild_id BIGINT,
    intro_message_id BIGINT,
    FOREIGN KEY (guild_id) REFERENCES guild_settings(guild_id)
);

-- Cria a tabela custom_roles (com chave primária composta)
CREATE TABLE IF NOT EXISTS custom_roles (
    user_id BIGINT,
    guild_id BIGINT,
    role_id BIGINT,
    PRIMARY KEY (user_id, guild_id), -- Chave primária composta
    FOREIGN KEY (guild_id) REFERENCES guild_settings(guild_id)
);

-- Adiciona chave estrangeira para selected_welcome_message_id (se não existir)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'fk_selected_welcome_message'
    ) THEN
        ALTER TABLE guild_settings
        ADD CONSTRAINT fk_selected_welcome_message
        FOREIGN KEY (selected_welcome_message_id)
        REFERENCES welcome_messages(id)
        ON DELETE SET NULL;
    END IF;
END $$;

-- Adiciona chave estrangeira para selected_goodbye_message_id (se não existir)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'fk_selected_goodbye_message'
    ) THEN
        ALTER TABLE guild_settings
        ADD CONSTRAINT fk_selected_goodbye_message
        FOREIGN KEY (selected_goodbye_message_id)
        REFERENCES goodbye_messages(id)
        ON DELETE SET NULL;
    END IF;
END $$;