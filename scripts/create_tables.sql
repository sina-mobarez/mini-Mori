-- migrations/create_tables.sql

-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    material TEXT,
    rating FLOAT,
    images TEXT[],
    code TEXT,
    brand_id INTEGER,
    brand_name TEXT,
    category_id INTEGER,
    category_name TEXT,
    gender_id INTEGER,
    gender_name TEXT,
    shop_id INTEGER,
    shop_name TEXT,
    link TEXT,
    status TEXT,
    colors TEXT[],
    sizes TEXT[],
    region TEXT,
    currency TEXT,
    current_price FLOAT,
    old_price FLOAT,
    off_percent INTEGER,
    update_date TEXT,
    search_vector tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('english', coalesce(name, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(description, '')), 'B') ||
        setweight(to_tsvector('english', coalesce(brand_name, '')), 'C') ||
        setweight(to_tsvector('english', coalesce(category_name, '')), 'C')
    ) STORED
);

-- Create index for full-text search
CREATE INDEX IF NOT EXISTS products_search_idx ON products USING GIN (search_vector);

-- Image embeddings table
CREATE TABLE IF NOT EXISTS image_embeddings (
    id TEXT PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    embedding vector(512) NOT NULL
);

-- Create indexes for image embeddings
CREATE INDEX IF NOT EXISTS image_embeddings_product_id_idx ON image_embeddings(product_id);
CREATE INDEX IF NOT EXISTS image_embeddings_embedding_idx ON image_embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);