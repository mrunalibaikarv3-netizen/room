-- ===========================================
-- ROOMCONNECT DATABASE
-- Part 1/2
-- ===========================================

-- Create Database
CREATE DATABASE IF NOT EXISTS roomconnect;

-- Use Database
USE roomconnect;

-- ===========================================
-- Owners Table
-- ===========================================

CREATE TABLE owners (

    owner_id INT AUTO_INCREMENT PRIMARY KEY,

    full_name VARCHAR(100) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    phone VARCHAR(15) NOT NULL,
    
    city VARCHAR(100) NOT NULL ,
    
    address TEXT NOT NULL ,

    password VARCHAR(255) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
    

);

-- ===========================================
-- Tenants Table
-- ===========================================

CREATE TABLE tenants (

    tenant_id INT AUTO_INCREMENT PRIMARY KEY,

    full_name VARCHAR(100) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    phone VARCHAR(15) NOT NULL,

    password VARCHAR(255) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ===========================================
-- Properties Table
-- ===========================================

CREATE TABLE properties (

    property_id INT AUTO_INCREMENT PRIMARY KEY,

    owner_id INT NOT NULL,

    title VARCHAR(150) NOT NULL,

    location VARCHAR(200) NOT NULL,

    room_type VARCHAR(50) NOT NULL,

    rent DECIMAL(10,2) NOT NULL,

    capacity INT NOT NULL,

    description TEXT,

    image VARCHAR(255),

    status ENUM('Available','Booked','Unavailable')
    DEFAULT 'Available',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (owner_id)
    REFERENCES owners(owner_id)
    ON DELETE CASCADE

);

-- ===========================================
-- Bookings Table
-- ===========================================

CREATE TABLE bookings (

    booking_id INT AUTO_INCREMENT PRIMARY KEY,

    property_id INT NOT NULL,

    owner_id INT NOT NULL,

    tenant_id INT NOT NULL,

    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    booking_status ENUM('Pending','Accepted','Rejected')
    DEFAULT 'Pending',

    FOREIGN KEY (property_id)
    REFERENCES properties(property_id)
    ON DELETE CASCADE,

    FOREIGN KEY (owner_id)
    REFERENCES owners(owner_id)
    ON DELETE CASCADE,

    FOREIGN KEY (tenant_id)
    REFERENCES tenants(tenant_id)
    ON DELETE CASCADE

);

-- ===========================================
-- Admin Table
-- ===========================================

CREATE TABLE admins (

    admin_id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL

);

-- ===========================================
-- Default Admin Account
-- ===========================================

INSERT INTO admins (username, password)
VALUES ('admin', 'admin123');

