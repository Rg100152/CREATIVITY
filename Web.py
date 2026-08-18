#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
CREATIVITY - Artistic Portfolio & Event Website
A surreal, dark-themed, single-file Flask Application built to match 
the exact aesthetics of the "Creativity never ends" landing page.
================================================================================
"""

import sqlite3
import json
import os
from flask import Flask, render_template_string, request, jsonify

# ==============================================================================
# 1. APPLICATION SETUP & CONFIGURATION
# ==============================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'creativity_surreal_key_2023'
DATABASE = 'creativity.db'

# ==============================================================================
# 2. DATABASE LAYER (SQLITE HELPER FUNCTIONS)
# ==============================================================================
def get_db_connection():
    """Establish and return a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database schema for the application."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Drop existing tables for clean seeding (safe for demonstration)
    cursor.execute("DROP TABLE IF EXISTS bookings")
    cursor.execute("DROP TABLE IF EXISTS contacts")
    cursor.execute("DROP TABLE IF EXISTS gallery")

    # Table: Gallery (Creative Artworks)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gallery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            image_url TEXT NOT NULL
        )
    ''')
    
    # Table: Ticket Bookings (Event Registrations)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            tickets INTEGER NOT NULL,
            booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table: Contact Messages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[INFO] Database schema initialized successfully.")

def seed_db():
    """Seed the database with rich dummy data for the gallery and event details."""
    conn = get_db_connection()
    cursor = conn.cursor()

    print("[INFO] Seeding database with rich artistic data...")
    
    # Seed Gallery Artworks (6 Entries to match the image aesthetic)
    gallery_data = [
        ('Dreamscape Portal', 'A surreal blend of dreamscapes and digital realities.', 'https://images.unsplash.com/photo-1541701494587-cb58502866ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('Floating Structures', 'Minimalist architectural concepts defying gravity.', 'https://images.unsplash.com/photo-1499781350541-7783f6c6a0c8?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('Abstract Harmony', 'Vibrant abstract artwork using geometric shapes.', 'https://images.unsplash.com/photo-1549880338-65ddcdfd017b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('Celestial Mechanics', 'An exploration of cosmic energy and orbital paths.', 'https://images.unsplash.com/photo-1518998053901-5348d3961a04?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('Liquid Reflections', 'Photography capturing the play of light in fluid motion.', 'https://images.unsplash.com/photo-1557672172-298e090bd0f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('Neon Illusions', 'Cyberpunk-inspired digital art with neon color palettes.', 'https://images.unsplash.com/photo-1550684848-fac1c5b4e853?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80')
    ]
    cursor.executemany('INSERT INTO gallery (title, description, image_url) VALUES (?, ?, ?)', gallery_data)
    
    conn.commit()
    conn.close()
    print("[INFO] Database seeding completed successfully.")

def get_gallery_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM gallery').fetchall()
    conn.close()
    return [dict(item) for item in items]

# ==============================================================================
# 3. MASSIVE HTML TEMPLATE STRING (INCLUDING CSS & JS)
# ==============================================================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Creativity | Surreal Art & Event Platform</title>
    <style>
        /* ====================================================================
               CSS RESET & GLOBAL STYLES
               ==================================================================== */
        *,
        *::before,
        *::after {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
            background-color: #121214;
            color: #F4F4F4;
            line-height: 1.7;
            overflow-x: hidden;
            background-image: radial-gradient(circle at 50% 0%, #262626 0%, #121214 60%);
        }

        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: #1A1A1A;
        }
        ::-webkit-scrollbar-thumb {
            background: #D4AF37;
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #B8952E;
        }

        a {
            text-decoration: none;
            color: inherit;
        }

        ul {
            list-style: none;
        }

        img {
            max-width: 100%;
            display: block;
        }

        .container {
            max-width: 1240px;
            margin: 0 auto;
            padding: 0 25px;
        }

        /* ====================================================================
               TYPOGRAPHY & GRADIENTS
               ==================================================================== */
        h1, h2, h3, h4 {
            font-weight: 700;
            margin-bottom: 20px;
            letter-spacing: -0.5px;
        }

        .gradient-text {
            background: linear-gradient(135deg, #eacda3 0%, #e2a76f 50%, #fceabd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .section-title {
            text-align: center;
            margin-bottom: 50px;
        }

        .section-title h2 {
            font-size: 40px;
        }

        .section-title p {
            color: #AAAAAA;
            font-size: 16px;
            letter-spacing: 3px;
            text-transform: uppercase;
        }

        /* ====================================================================
               BUTTONS & INTERACTIVE ELEMENTS
               ==================================================================== */
        .btn-border {
            display: inline-block;
            padding: 12px 28px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            color: #FFFFFF;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 1px;
            background: transparent;
            cursor: pointer;
            backdrop-filter: blur(4px);
            position: relative;
            overflow: hidden;
        }

        .btn-border:hover {
            border-color: #e2a76f;
            color: #e2a76f;
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
        }

        .btn-border::after {
            content: '';
            position: absolute;
            width: 0;
            height: 100%;
            top: 0;
            left: 0;
            background: rgba(255, 255, 255, 0.05);
            transition: width 0.4s;
        }
        .btn-border:hover::after {
            width: 100%;
        }

        /* ====================================================================
               HEADER & NAVIGATION
               ==================================================================== */
        header {
            padding: 25px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            backdrop-filter: blur(12px);
            background: rgba(18, 18, 20, 0.85);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        header .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo svg {
            width: 32px;
            height: 32px;
            fill: #FFFFFF;
        }

        .logo span {
            font-size: 24px;
            font-weight: 700;
            color: #FFFFFF;
        }

        nav {
            display: flex;
            align-items: center;
            gap: 35px;
        }

        nav ul {
            display: flex;
            gap: 30px;
        }

        nav ul li a {
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #B0B0B0;
            position: relative;
        }

        nav ul li a:hover {
            color: #FFFFFF;
        }

        nav ul li a::after {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            bottom: -5px;
            left: 0;
            background: linear-gradient(90deg, #eacda3, #e2a76f);
            transition: width 0.4s ease;
        }

        nav ul li a:hover::after {
            width: 100%;
        }

        .login-btn {
            padding: 8px 20px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: #FFFFFF;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 13px;
            background: transparent;
            cursor: pointer;
            border-radius: 2px;
        }

        .login-btn:hover {
            border-color: #e2a76f;
            background: rgba(226, 167, 111, 0.1);
        }

        /* ====================================================================
               HERO SECTION
               ==================================================================== */
        .hero {
            padding: 80px 0 60px;
            min-height: 90vh;
            display: flex;
            align-items: center;
        }

        .hero .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 60px;
            width: 100%;
        }

        /* Hero Text Left Side */
        .hero-text {
            flex: 1;
        }

        .hero-text h1 {
            font-size: 70px;
            line-height: 1.1;
            margin-bottom: 25px;
        }

        .hero-text h1 .line1 {
            display: block;
            color: #FFFFFF;
            -webkit-text-fill-color: #FFFFFF;
        }

        .hero-text h1 .line2 {
            display: block;
        }

        .hero-text p {
            font-size: 16px;
            color: #A0A0A0;
            max-width: 450px;
            margin-bottom: 40px;
            line-height: 1.8;
        }

        /* Hero Visual Right Side (Surreal Artwork) */
        .hero-visual {
            flex: 1;
            position: relative;
            height: 500px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* Surreal Cloud Head CSS Art */
        .cloud-art-container {
            position: relative;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .cloud-figure {
            position: relative;
            width: 180px;
            height: 200px;
            background: transparent;
        }

        .cloud-head {
            width: 180px;
            height: 120px;
            background: #FFFFFF;
            border-radius: 50% 50% 30% 70% / 30% 40% 60% 70%;
            position: absolute;
            top: 10px;
            left: 0;
            box-shadow: 0 20px 60px rgba(255, 255, 255, 0.15);
            filter: blur(0.5px);
            animation: floatCloud 6s ease-in-out infinite alternate;
        }

        .cloud-head::before, .cloud-head::after {
            content: '';
            position: absolute;
            background: #FFFFFF;
            border-radius: 50%;
            opacity: 0.8;
        }
        .cloud-head::before {
            width: 100px;
            height: 70px;
            top: -25px;
            left: 20px;
        }
        .cloud-head::after {
            width: 120px;
            height: 80px;
            top: -15px;
            right: 10px;
        }

        .cloud-body {
            position: absolute;
            bottom: 0;
            left: 40px;
            width: 100px;
            height: 120px;
            background: #2d2d2d;
            border-radius: 10px 10px 40px 40px / 10px 10px 60px 60px;
            background-image: linear-gradient(to bottom, #3a3a3a, #1a1a1a);
            box-shadow: inset -5px 0 15px rgba(0,0,0,0.8);
            z-index: -1;
        }

        @keyframes floatCloud {
            0% { transform: translateY(0px) rotate(-2deg); }
            100% { transform: translateY(-15px) rotate(2deg); }
        }

        /* Orbiting Rings */
        .orbit-ring {
            position: absolute;
            width: 350px;
            height: 120px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 50%;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-15deg);
            animation: rotateRing 20s linear infinite;
        }

        .orbit-ring:nth-child(2) {
            width: 250px;
            height: 90px;
            border: 1px solid rgba(255, 215, 0, 0.2);
            transform: translate(-50%, -50%) rotate(25deg);
            animation-duration: 15s;
            animation-direction: reverse;
        }

        .orbit-ring:nth-child(3) {
            width: 420px;
            height: 140px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            transform: translate(-50%, -50%) rotate(-45deg);
            animation-duration: 25s;
        }

        @keyframes rotateRing {
            from { transform: translate(-50%, -50%) rotate(-15deg) rotateX(60deg); }
            to { transform: translate(-50%, -50%) rotate(345deg) rotateX(60deg); }
        }

        /* Floating Planets / Geometric Elements */
        .planet-item {
            position: absolute;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #e2a76f;
            box-shadow: 0 0 20px rgba(226, 167, 111, 0.3);
            z-index: 2;
        }
        .planet-item:nth-child(4) { left: 10%; top: 60%; animation: floatOrb 4s ease-in-out infinite alternate; }
        .planet-item:nth-child(5) { right: 10%; top: 20%; background: #b8952e; width: 30px; height: 30px; animation: floatOrb 5s ease-in-out infinite alternate-reverse; }
        .planet-item:nth-child(6) { left: 30%; bottom: 10%; background: #d4af37; width: 15px; height: 15px; animation: floatOrb 3.5s ease-in-out infinite alternate; }

        @keyframes floatOrb {
            0% { transform: translateY(0px) scale(1); }
            100% { transform: translateY(-20px) scale(1.1); }
        }

        /* Paper Airplanes (CSS Art) */
        .paper-plane {
            position: absolute;
            width: 0;
            height: 0;
            border-top: 15px solid transparent;
            border-bottom: 15px solid transparent;
            border-right: 25px solid rgba(255, 255, 255, 0.6);
            transform: rotate(-20deg);
            z-index: 3;
            animation: planeFly 8s linear infinite;
        }
        .paper-plane::after {
            content: '';
            position: absolute;
            top: -15px;
            left: -5px;
            width: 0;
            height: 0;
            border-top: 15px solid transparent;
            border-bottom: 15px solid transparent;
            border-right: 25px solid rgba(226, 167, 111, 0.7);
        }
        
        .paper-plane:nth-child(7) { top: 20%; left: 20%; transform: rotate(-30deg); animation-duration: 10s; }
        .paper-plane:nth-child(8) { top: 70%; right: 20%; transform: rotate(120deg); animation-duration: 7s; }

        @keyframes planeFly {
            0% { transform: translate(0, 0) rotate(-30deg) scale(1); opacity: 0.5; }
            50% { transform: translate(50px, -50px) rotate(-20deg) scale(1.2); opacity: 1; }
            100% { transform: translate(-30px, 30px) rotate(-40deg) scale(0.8); opacity: 0.3; }
        }

        /* Date Display & Social Media Elements */
        .hero-date {
            position: absolute;
            right: 0;
            bottom: 0;
            text-align: right;
            color: #FFFFFF;
        }
        .hero-date .day { font-size: 48px; font-weight: 700; line-height: 1; display: block; }
        .hero-date .month-year { font-size: 18px; font-weight: 300; letter-spacing: 1px; opacity: 0.8; }

        .hero-socials {
            position: absolute;
            bottom: -30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 20px;
        }

        .hero-socials a svg {
            width: 20px;
            height: 20px;
            fill: #AAAAAA;
            transition: fill 0.3s, transform 0.3s;
        }
        .hero-socials a:hover svg {
            fill: #e2a76f;
            transform: translateY(-3px);
        }

        /* Plus Icon Button (Bottom Right) */
        .plus-btn {
            position: absolute;
            right: 0;
            bottom: -30px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: 1px solid #e2a76f;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #e2a76f;
            font-size: 28px;
            font-weight: 300;
            cursor: pointer;
            transition: 0.3s;
            background: transparent;
        }
        .plus-btn:hover {
            background: #e2a76f;
            color: #121214;
            transform: scale(1.1) rotate(90deg);
        }

        /* ====================================================================
               ABOUT SECTION
               ==================================================================== */
        .about-section {
            padding: 100px 0;
            background: rgba(255, 255, 255, 0.02);
        }

        .about-section .container {
            display: flex;
            gap: 60px;
            align-items: center;
        }

        .about-text {
            flex: 1;
        }

        .about-text h2 {
            font-size: 44px;
            margin-bottom: 30px;
        }

        .about-text p {
            color: #B0B0B0;
            margin-bottom: 30px;
            font-size: 16px;
        }

        .about-counters {
            display: flex;
            gap: 50px;
        }

        .counter-box {
            text-align: left;
        }
        .counter-box .num {
            font-size: 40px;
            font-weight: 700;
            color: #e2a76f;
            display: block;
        }
        .counter-box span {
            font-size: 14px;
            color: #AAAAAA;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .about-visual {
            flex: 1;
            position: relative;
            height: 400px;
            background: linear-gradient(135deg, rgba(226, 167, 111, 0.1), rgba(255, 255, 255, 0.05));
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .about-visual h3 {
            font-size: 36px;
            text-align: center;
            opacity: 0.2;
            transform: rotate(-10deg);
        }

        /* ====================================================================
               GALLERY SECTION
               ==================================================================== */
        .gallery-section {
            padding: 100px 0;
            background: #121214;
        }

        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 25px;
        }

        .gallery-card {
            position: relative;
            border-radius: 12px;
            overflow: hidden;
            background: #1A1A1A;
            cursor: pointer;
            height: 300px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .gallery-card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        .gallery-card:hover img {
            transform: scale(1.15);
        }

        .gallery-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, transparent 100%);
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            padding: 25px;
            opacity: 0;
            transition: opacity 0.5s ease;
        }

        .gallery-card:hover .gallery-overlay {
            opacity: 1;
        }

        .gallery-overlay h4 {
            font-size: 22px;
            color: #FFFFFF;
            margin-bottom: 5px;
        }

        .gallery-overlay p {
            font-size: 14px;
            color: #CCCCCC;
        }

        /* Lightbox Modal */
        .lightbox {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            z-index: 9999;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }

        .lightbox.active {
            display: flex;
        }

        .lightbox img {
            max-width: 80%;
            max-height: 80%;
            border-radius: 8px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.8);
            animation: zoomIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        @keyframes zoomIn {
            from { transform: scale(0.8); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }

        .lightbox-close {
            position: absolute;
            top: 30px;
            right: 40px;
            font-size: 40px;
            color: #FFFFFF;
            cursor: pointer;
            transition: 0.3s;
        }
        .lightbox-close:hover {
            transform: rotate(90deg);
            color: #e2a76f;
        }

        .lightbox-text {
            color: #FFFFFF;
            margin-top: 20px;
            text-align: center;
        }
        .lightbox-text h3 { font-size: 28px; margin-bottom: 5px; }
        .lightbox-text p { font-size: 16px; color: #AAAAAA; }

        /* ====================================================================
               TICKET MODAL SECTION
               ==================================================================== */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 10000;
            justify-content: center;
            align-items: center;
            backdrop-filter: blur(6px);
        }

        .modal-overlay.active {
            display: flex;
        }

        .modal-content {
            background: #1A1A1A;
            padding: 40px;
            border-radius: 12px;
            width: 100%;
            max-width: 450px;
            border: 1px solid rgba(226, 167, 111, 0.3);
            position: relative;
            animation: slideUp 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        @keyframes slideUp {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        .modal-content h2 {
            color: #FFFFFF;
            margin-bottom: 30px;
            text-align: center;
        }
        .modal-content h2 span { color: #e2a76f; }

        .modal-close {
            position: absolute;
            top: 15px;
            right: 20px;
            font-size: 30px;
            color: #AAAAAA;
            cursor: pointer;
            transition: 0.3s;
        }
        .modal-close:hover {
            color: #FFFFFF;
            transform: rotate(90deg);
        }

        .modal-content .form-group {
            margin-bottom: 20px;
        }

        .modal-content label {
            display: block;
            color: #CCCCCC;
            font-size: 14px;
            margin-bottom: 8px;
            font-weight: 600;
        }

        .modal-content input, .modal-content textarea {
            width: 100%;
            padding: 12px 15px;
            background: #222222;
            border: 1px solid #333333;
            color: #FFFFFF;
            border-radius: 4px;
            outline: none;
            font-size: 16px;
            transition: 0.3s;
        }

        .modal-content input:focus, .modal-content textarea:focus {
            border-color: #e2a76f;
            box-shadow: 0 0 15px rgba(226, 167, 111, 0.1);
        }

        .modal-content .btn-submit {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #eacda3, #e2a76f);
            border: none;
            color: #121214;
            font-weight: 700;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
            transition: 0.3s;
        }
        .modal-content .btn-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(226, 167, 111, 0.3);
        }

        .ticket-msg-success {
            display: none;
            color: #d4edda;
            text-align: center;
            margin-top: 15px;
            font-size: 14px;
        }
        .ticket-msg-error {
            display: none;
            color: #f8d7da;
            text-align: center;
            margin-top: 15px;
            font-size: 14px;
        }

        /* ====================================================================
               CONTACT SECTION
               ==================================================================== */
        .contact-section {
            padding: 100px 0;
            background: rgba(255, 255, 255, 0.02);
        }

        .contact-wrapper {
            display: flex;
            gap: 60px;
            align-items: flex-start;
        }

        .contact-info {
            flex: 1;
        }
        .contact-info h2 { font-size: 40px; margin-bottom: 20px; }
        .contact-info p { color: #B0B0B0; font-size: 16px; margin-bottom: 30px; }

        .contact-form {
            flex: 1.5;
        }
        .contact-form input, .contact-form textarea {
            width: 100%;
            padding: 15px;
            background: #1A1A1A;
            border: 1px solid #333;
            color: #FFFFFF;
            border-radius: 6px;
            margin-bottom: 20px;
            font-size: 16px;
            outline: none;
            transition: 0.3s;
        }

        .contact-form textarea { min-height: 150px; resize: vertical; }

        .contact-form input:focus, .contact-form textarea:focus {
            border-color: #e2a76f;
            box-shadow: 0 0 20px rgba(226, 167, 111, 0.1);
            background: #222222;
        }

        .contact-form button {
            padding: 14px 40px;
            background: transparent;
            border: 1px solid #e2a76f;
            color: #e2a76f;
            font-weight: 700;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
            transition: 0.3s;
            text-transform: uppercase;
        }

        .contact-form button:hover {
            background: #e2a76f;
            color: #121214;
        }

        .contact-msg {
            display: none;
            margin-top: 15px;
            font-size: 14px;
            text-align: center;
        }
        .contact-msg.success { color: #d4edda; display: block; }
        .contact-msg.error { color: #f8d7da; display: block; }

        /* ====================================================================
               FOOTER
               ==================================================================== */
        footer {
            background: #0A0A0A;
            padding: 50px 0 30px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            text-align: center;
        }

        footer p {
            color: #666666;
            font-size: 14px;
        }
        footer .footer-logo {
            font-size: 24px;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 15px;
            display: block;
        }
        footer .footer-logo span { color: #e2a76f; }
        footer .social-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
        footer .social-links a svg {
            width: 20px;
            height: 20px;
            fill: #666666;
            transition: 0.3s;
        }
        footer .social-links a:hover svg { fill: #e2a76f; transform: translateY(-3px); }

        /* ====================================================================
               RESPONSIVE MEDIA QUERIES
               ==================================================================== */
        @media screen and (max-width: 992px) {
            .hero .container { flex-direction: column; text-align: center; }
            .hero-text p { margin: 0 auto 40px; }
            .hero-visual { height: 450px; width: 100%; }
            .hero-date, .plus-btn, .hero-socials { position: relative; bottom: auto; right: auto; left: auto; margin-top: 20px; text-align: center; justify-content: center; }
            .hero-date { display: flex; gap: 10px; justify-content: center; align-items: baseline; }
            .hero-date .day { font-size: 32px; }
            .about-section .container { flex-direction: column; }
            .about-counters { justify-content: center; }
            .gallery-grid { grid-template-columns: repeat(2, 1fr); }
            .contact-wrapper { flex-direction: column; }
            nav ul { display: none; } /* Simplified for mobile demo */
            nav .login-btn { display: none; }
        }

        @media screen and (max-width: 768px) {
            .hero-text h1 { font-size: 44px; }
            .hero-visual { height: 350px; }
            .orbit-ring { width: 250px; height: 90px; }
            .orbit-ring:nth-child(3) { width: 300px; height: 100px; }
            .gallery-grid { grid-template-columns: 1fr; }
        }

        @media screen and (max-width: 480px) {
            .hero-text h1 { font-size: 34px; }
            .section-title h2 { font-size: 30px; }
            .modal-content { margin: 20px; padding: 25px; }
        }
        /* End CSS */
    </style>
</head>
<body>

    <!-- ================================================================
    HEADER & NAVIGATION
    ================================================================ -->
    <header>
        <div class="container">
            <div class="logo">
                <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/></svg>
                <span>CREATIVITY</span>
            </div>
            <nav>
                <ul>
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#gallery">Gallery</a></li>
                    <li><a href="#ticket-btn">Event</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
                <button class="login-btn" onclick="alert('Login functionality is not implemented in this demo.')">Login</button>
            </nav>
        </div>
    </header>

    <!-- ================================================================
    HERO SECTION
    ================================================================ -->
    <section class="hero" id="home">
        <div class="container">
            <div class="hero-text">
                <h1>
                    <span class="line1">Creativity</span>
                    <span class="line2 gradient-text">never ends</span>
                </h1>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
                <button class="btn-border" onclick="openTicketModal()">TICKETS</button>
            </div>
            <div class="hero-visual">
                <!-- Surreal CSS Art Centerpiece -->
                <div class="cloud-art-container">
                    <div class="cloud-figure">
                        <!-- Orbit Rings -->
                        <div class="orbit-ring"></div>
                        <div class="orbit-ring"></div>
                        <div class="orbit-ring"></div>
                        <!-- Floating Planets -->
                        <div class="planet-item"></div>
                        <div class="planet-item"></div>
                        <div class="planet-item"></div>
                        <!-- Paper Airplanes -->
                        <div class="paper-plane"></div>
                        <div class="paper-plane"></div>
                        
                        <!-- The Cloud Head & Body -->
                        <div class="cloud-head"></div>
                        <div class="cloud-body"></div>
                    </div>
                </div>

                <!-- Bottom Right Date -->
                <div class="hero-date">
                    <span class="day">10</span>
                    <span class="month-year">October<br>2023</span>
                </div>

                <!-- Social Media Links -->
                <div class="hero-socials">
                    <a href="#"><svg viewBox="0 0 24 24"><path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"/></svg></a>
                    <a href="#"><svg viewBox="0 0 24 24"><path d="M5 3h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zm13 2h-2.5A3.5 3.5 0 0 0 12 8.5V11h-2v3h2v7h3v-7h3v-3h-3V9a1 1 0 0 1 1-1h2V5z"/></svg></a>
                    <a href="#"><svg viewBox="0 0 24 24"><path d="M4.98 3.5c0 1.38-1.12 2.5-2.5 2.5S0 4.88 0 3.5 1.12 1 2.48 1s2.5 1.12 2.5 2.5zM.5 5h4v14h-4V5zM20.5 9.5c0-3-1.8-4.5-4.5-4.5-1.6 0-2.8.7-3.5 1.7V5h-4v14h4v-9c0-1 .5-2 2-2s2 1 2 2v9h4v-9.5z"/></svg></a>
                </div>

                <!-- Plus Button -->
                <button class="plus-btn">+</button>
            </div>
        </div>
    </section>

    <!-- ================================================================
    ABOUT SECTION
    ================================================================ -->
    <section class="about-section" id="about">
        <div class="container">
            <div class="about-text">
                <h2>About the <span class="gradient-text">Creativity</span></h2>
                <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.</p>
                <p>Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.</p>
                <div class="about-counters">
                    <div class="counter-box">
                        <span class="num" data-target="150">0</span>
                        <span>Projects Completed</span>
                    </div>
                    <div class="counter-box">
                        <span class="num" data-target="45">0</span>
                        <span>Artists Worldwide</span>
                    </div>
                    <div class="counter-box">
                        <span class="num" data-target="12">0</span>
                        <span>Global Awards</span>
                    </div>
                </div>
            </div>
            <div class="about-visual">
                <h3>SURREAL<br>ABSTRACT<br>ART</h3>
            </div>
        </div>
    </section>

    <!-- ================================================================
    GALLERY SECTION
    ================================================================ -->
    <section class="gallery-section" id="gallery">
        <div class="container">
            <div class="section-title">
                <p>Our Gallery</p>
                <h2 class="gradient-text">Creative Artworks</h2>
            </div>
            <div class="gallery-grid">
                {% for item in gallery %}
                <div class="gallery-card" onclick="openLightbox('{{ item.image_url }}', '{{ item.title }}', '{{ item.description }}')">
                    <img src="{{ item.image_url }}" alt="{{ item.title }}">
                    <div class="gallery-overlay">
                        <h4>{{ item.title }}</h4>
                        <p>{{ item.description }}</p>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <!-- ================================================================
    TICKET MODAL (Hidden by default)
    ================================================================ -->
    <div class="modal-overlay" id="ticketModal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeTicketModal()">&times;</span>
            <h2>Book <span class="gradient-text">Tickets</span></h2>
            <form id="ticketForm">
                <div class="form-group">
                    <label>Full Name</label>
                    <input type="text" name="name" placeholder="Your full name" required>
                </div>
                <div class="form-group">
                    <label>Email Address</label>
                    <input type="email" name="email" placeholder="your@email.com" required>
                </div>
                <div class="form-group">
                    <label>Number of Tickets</label>
                    <input type="number" name="tickets" value="1" min="1" max="10" required>
                </div>
                <button type="submit" class="btn-submit">Confirm Booking</button>
                <div id="ticketSuccess" class="ticket-msg-success">Tickets booked successfully! We'll send you a confirmation email shortly.</div>
                <div id="ticketError" class="ticket-msg-error">An error occurred. Please try again.</div>
            </form>
        </div>
    </div>

    <!-- ================================================================
    LIGHTBOX MODAL (Hidden by default)
    ================================================================ -->
    <div class="lightbox" id="lightboxModal">
        <span class="lightbox-close" onclick="closeLightbox()">&times;</span>
        <img id="lightboxImage" src="" alt="Artwork">
        <div class="lightbox-text">
            <h3 id="lightboxTitle">Title</h3>
            <p id="lightboxDesc">Description</p>
        </div>
    </div>

    <!-- ================================================================
    CONTACT SECTION
    ================================================================ -->
    <section class="contact-section" id="contact">
        <div class="container">
            <div class="contact-wrapper">
                <div class="contact-info">
                    <h2>Let's <span class="gradient-text">Connect</span></h2>
                    <p>Whether you have a question about our upcoming events, need custom artwork commissions, or simply want to collaborate, we are always open to discussing new creative projects. Drop us a message and we will get back to you within 24 hours.</p>
                    <p><strong>Email:</strong> hello@creativityart.com<br><strong>Phone:</strong> +1 (555) 789-1011</p>
                </div>
                <form class="contact-form" id="contactForm">
                    <input type="text" name="name" placeholder="Your Name" required>
                    <input type="email" name="email" placeholder="Your Email" required>
                    <textarea name="message" placeholder="Your Message..." required></textarea>
                    <button type="submit">Send Message</button>
                    <div id="contactMsgSuccess" class="contact-msg success">Your message has been sent successfully!</div>
                    <div id="contactMsgError" class="contact-msg error">Failed to send message. Please try again later.</div>
                </form>
            </div>
        </div>
    </section>

    <!-- ================================================================
    FOOTER
    ================================================================ -->
    <footer>
        <div class="container">
            <span class="footer-logo">CREA<span>TIVITY</span></span>
            <p>&copy; 2023 Creativity Art Studio. Designed for the surreal thinkers.<br>All rights reserved. Made with passion.</p>
            <div class="social-links">
                <a href="#"><svg viewBox="0 0 24 24"><path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"/></svg></a>
                <a href="#"><svg viewBox="0 0 24 24"><path d="M5 3h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zm13 2h-2.5A3.5 3.5 0 0 0 12 8.5V11h-2v3h2v7h3v-7h3v-3h-3V9a1 1 0 0 1 1-1h2V5z"/></svg></a>
                <a href="#"><svg viewBox="0 0 24 24"><path d="M4.98 3.5c0 1.38-1.12 2.5-2.5 2.5S0 4.88 0 3.5 1.12 1 2.48 1s2.5 1.12 2.5 2.5zM.5 5h4v14h-4V5zM20.5 9.5c0-3-1.8-4.5-4.5-4.5-1.6 0-2.8.7-3.5 1.7V5h-4v14h4v-9c0-1 .5-2 2-2s2 1 2 2v9h4v-9.5z"/></svg></a>
            </div>
        </div>
    </footer>

    <!-- ================================================================
    JAVASCRIPT LOGIC (ANIMATIONS, MODALS, AJAX)
    ================================================================ -->
    <script>
        (function() {
            "use strict";

            // -----------------------------------------------------------------
            // 1. TICKET BOOKING MODAL
            // -----------------------------------------------------------------
            window.openTicketModal = function() {
                document.getElementById('ticketModal').classList.add('active');
                document.body.style.overflow = 'hidden';
            };

            window.closeTicketModal = function() {
                document.getElementById('ticketModal').classList.remove('active');
                document.body.style.overflow = 'auto';
            };

            // Close modal on outside click
            document.getElementById('ticketModal').addEventListener('click', function(e) {
                if (e.target === this) {
                    closeTicketModal();
                }
            });

            // -----------------------------------------------------------------
            // 2. LIGHTBOX GALLERY
            // -----------------------------------------------------------------
            window.openLightbox = function(url, title, desc) {
                document.getElementById('lightboxImage').src = url;
                document.getElementById('lightboxTitle').textContent = title;
                document.getElementById('lightboxDesc').textContent = desc;
                document.getElementById('lightboxModal').classList.add('active');
                document.body.style.overflow = 'hidden';
            };

            window.closeLightbox = function() {
                document.getElementById('lightboxModal').classList.remove('active');
                document.body.style.overflow = 'auto';
            };

            // Close lightbox on outside click
            document.getElementById('lightboxModal').addEventListener('click', function(e) {
                if (e.target === this) {
                    closeLightbox();
                }
            });

            // -----------------------------------------------------------------
            // 3. COUNTER ANIMATION (Intersection Observer)
            // -----------------------------------------------------------------
            const counters = document.querySelectorAll('.counter-box .num');
            const speed = 200;

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const el = entry.target;
                        const updateCount = () => {
                            const target = parseInt(el.getAttribute('data-target'));
                            const count = parseInt(el.innerText);
                            const increment = Math.ceil(target / speed);
                            if (count < target) {
                                el.innerText = count + increment;
                                setTimeout(updateCount, 30);
                            } else {
                                el.innerText = target + '+';
                            }
                        };
                        updateCount();
                        observer.unobserve(el);
                    }
                });
            }, { threshold: 0.5 });

            counters.forEach(counter => observer.observe(counter));

            // -----------------------------------------------------------------
            // 4. TICKET FORM AJAX SUBMISSION
            // -----------------------------------------------------------------
            document.getElementById('ticketForm').addEventListener('submit', function(e) {
                e.preventDefault();
                const formData = new FormData(this);
                const successMsg = document.getElementById('ticketSuccess');
                const errorMsg = document.getElementById('ticketError');

                // Clear previous messages
                successMsg.style.display = 'none';
                errorMsg.style.display = 'none';

                fetch('/api/book', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        successMsg.style.display = 'block';
                        document.getElementById('ticketForm').reset();
                        setTimeout(() => {
                            closeTicketModal();
                            successMsg.style.display = 'none';
                        }, 3000);
                    } else {
                        errorMsg.style.display = 'block';
                    }
                })
                .catch(err => {
                    console.error(err);
                    errorMsg.style.display = 'block';
                });
            });

            // -----------------------------------------------------------------
            // 5. CONTACT FORM AJAX SUBMISSION
            // -----------------------------------------------------------------
            document.getElementById('contactForm').addEventListener('submit', function(e) {
                e.preventDefault();
                const formData = new FormData(this);
                const successMsg = document.getElementById('contactMsgSuccess');
                const errorMsg = document.getElementById('contactMsgError');

                successMsg.classList.remove('success');
                errorMsg.classList.remove('error');
                successMsg.style.display = 'none';
                errorMsg.style.display = 'none';

                fetch('/api/contact', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        successMsg.style.display = 'block';
                        successMsg.classList.add('success');
                        document.getElementById('contactForm').reset();
                        setTimeout(() => {
                            successMsg.style.display = 'none';
                        }, 5000);
                    } else {
                        errorMsg.style.display = 'block';
                        errorMsg.classList.add('error');
                    }
                })
                .catch(err => {
                    console.error(err);
                    errorMsg.style.display = 'block';
                    errorMsg.classList.add('error');
                });
            });

        })();
    </script>
</body>
</html>
"""

# ==============================================================================
# 4. ROUTES & CONTROLLERS
# ==============================================================================
@app.route('/')
def index():
    """Render the creative artistic portfolio homepage."""
    try:
        gallery_items = get_gallery_items()
    except Exception as e:
        print(f"[ERROR] Failed to fetch gallery data: {e}")
        gallery_items = []
    
    return render_template_string(
        HTML_TEMPLATE,
        gallery=gallery_items
    )

@app.route('/api/book', methods=['POST'])
def book_tickets():
    """Handle AJAX ticket booking request."""
    name = request.form.get('name')
    email = request.form.get('email')
    tickets = request.form.get('tickets')
    
    if not name or not email or not tickets:
        return jsonify({'success': False, 'message': 'All fields are required.'})
    
    try:
        tickets = int(tickets)
        if tickets < 1:
            raise ValueError
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid ticket quantity.'})
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO bookings (name, email, tickets) VALUES (?, ?, ?)', (name, email, tickets))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Booking confirmed!'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Handle AJAX contact form submission."""
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    if not name or not email or not message:
        return jsonify({'success': False, 'message': 'All fields are required.'})
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)', (name, email, message))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Message sent!'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)})

# ==============================================================================
# 5. MAIN EXECUTION BLOCK
# ==============================================================================
if __name__ == '__main__':
    print("=" * 60)
    print("           CREATIVITY - Surreal Art & Event Platform")
    print("                     Production Server")
    print("=" * 60)
    
    # Initialize and seed the database if it doesn't exist
    if not os.path.exists(DATABASE):
        print("[INFO] Database not found. Initializing and seeding...")
        init_db()
        seed_db()
    else:
        # Ensure schema is valid
        try:
            conn = sqlite3.connect(DATABASE)
            conn.execute('SELECT 1 FROM gallery LIMIT 1')
            conn.close()
        except sqlite3.OperationalError:
            print("[WARNING] Existing database schema outdated. Re-creating and seeding...")
            os.remove(DATABASE)
            init_db()
            seed_db()
            
    print("[INFO] Starting Flask development server...")
    print("[INFO] Access the website at: http://127.0.0.1:5000")
    print("[INFO] Press CTRL+C to stop the server.")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
