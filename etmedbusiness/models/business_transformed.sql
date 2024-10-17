{{ config(materialized='table') }}

WITH source_data AS (
    -- Select the columns you need, excluding 'channel_title'
    SELECT DISTINCT
        id,
        REPLACE(channel_username, '@', '') AS channel_username,  -- Remove '@' from channel_username
        message,
        DATE(date) AS date  -- Extract only year, month, and day from date
    FROM {{ source('public', 'medbusiness') }} -- Reference the source table
),

-- Filter only data related to 'lobelia4cosmetics'
lobelia_data AS (
    SELECT 
        id,
        channel_username,
        message,
        date
    FROM source_data
    WHERE channel_username = 'lobelia4cosmetics'
),

-- Extract product, price, and address from the message column
business_data AS (
    SELECT 
        id,
        channel_username,
        date,
        -- Extract product
        SUBSTRING(message FROM '^(.*?)(\n|$)') As product,
        -- Extract price 
        SUBSTRING(message FROM 'Price\s*([0-9]+(?:,?[0-9]*)(?:\.\d+)?)') AS price,
        -- Extract address 
        SUBSTRING(message FROM '(?:Adress|Address):-\s*(.+?school)') AS address
    FROM lobelia_data

)

-- Final selection of transformed data, dropping the 'message' column
SELECT 
    id,
    channel_username,
    date,
    product,
    price,
    address
FROM business_data

WHERE 
    price IS NOT NULL
