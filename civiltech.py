import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from forms import ContactForm, ServiceInquiryForm

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize CSRF protection
csrf = CSRFProtect(app)

@app.route('/')
def index():
    """Homepage with overview and key features"""
    return render_template('index.html')

@app.route('/products')
def products():
    """Products catalog with detailed specifications"""
    return render_template('products.html')

@app.route('/services')
def services():
    """Services page with inquiry form"""
    form = ServiceInquiryForm()
    return render_template('services.html', form=form)

@app.route('/services', methods=['POST'])
def services_post():
    """Handle service inquiry form submission"""
    form = ServiceInquiryForm()
    
    if form.validate_on_submit():
        # Process the service inquiry
        app.logger.info("🔧 New Service Inquiry Submission:")
        app.logger.info(f"Company: {form.company.data}")
        app.logger.info(f"Contact: {form.name.data}")
        app.logger.info(f"Email: {form.email.data}")
        app.logger.info(f"Phone: {form.phone.data}")
        app.logger.info(f"Service Type: {form.service_type.data}")
        app.logger.info(f"Project Details: {form.project_details.data}")
        
        flash('Thank you for your service inquiry! Our team will contact you within 24 hours.', 'success')
        return redirect(url_for('services'))
    
    # If form validation fails, re-render with errors
    return render_template('services.html', form=form)

@app.route('/about')
def about():
    """About us page with company information and team"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact page with contact form"""
    form = ContactForm()
    return render_template('contact.html', form=form)

@app.route('/contact', methods=['POST'])
def contact_post():
    """Handle contact form submission"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # Process the contact form
        app.logger.info("📨 New Contact Form Submission:")
        app.logger.info(f"Name: {form.name.data}")
        app.logger.info(f"Email: {form.email.data}")
        app.logger.info(f"Subject: {form.subject.data}")
        app.logger.info(f"Message: {form.message.data}")
        
        flash('Thank you for contacting us! We will respond to your message shortly.', 'success')
        return redirect(url_for('contact'))
    
    # If form validation fails, re-render with errors
    return render_template('contact.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('base.html', error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('base.html', error_message="Internal server error"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, EmailField, TelField
from wtforms.validators import DataRequired, Email, Length, Optional

class ContactForm(FlaskForm):
    """Contact form with validation"""
    name = StringField('Full Name', validators=[
        DataRequired(message='Please enter your full name'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    email = EmailField('Email Address', validators=[
        DataRequired(message='Please enter your email address'),
        Email(message='Please enter a valid email address')
    ])
    
    subject = StringField('Subject', validators=[
        DataRequired(message='Please enter a subject'),
        Length(min=5, max=200, message='Subject must be between 5 and 200 characters')
    ])
    
    message = TextAreaField('Message', validators=[
        DataRequired(message='Please enter your message'),
        Length(min=10, max=2000, message='Message must be between 10 and 2000 characters')
    ])

class ServiceInquiryForm(FlaskForm):
    """Service inquiry form for custom quotes"""
    company = StringField('Company Name', validators=[
        DataRequired(message='Please enter your company name'),
        Length(min=2, max=150, message='Company name must be between 2 and 150 characters')
    ])
    
    name = StringField('Contact Person', validators=[
        DataRequired(message='Please enter the contact person name'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    email = EmailField('Email Address', validators=[
        DataRequired(message='Please enter your email address'),
        Email(message='Please enter a valid email address')
    ])
    
    phone = TelField('Phone Number', validators=[
        Optional(),
        Length(min=10, max=20, message='Phone number must be between 10 and 20 characters')
    ])
    
    service_type = SelectField('Service Type', choices=[
        ('', 'Select a service type...'),
        ('structural_testing', 'Structural Load & Response Testing'),
        ('ndt_inspection', 'Non-Destructive Testing & Inspection'),
        ('geotechnical_testing', 'Geotechnical & Foundation Testing'),
        ('custom_solution', 'Custom Testing Solution'),
        ('equipment_rental', 'Equipment Rental'),
        ('training_certification', 'Training & Certification'),
        ('consultation', 'Engineering Consultation')
    ], validators=[
        DataRequired(message='Please select a service type')
    ])
    
    project_details = TextAreaField('Project Details', validators=[
        DataRequired(message='Please provide project details'),
        Length(min=20, max=3000, message='Project details must be between 20 and 3000 characters')
    ])
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{% block meta_description %}Civil Structure Test Tech provides innovative testing tools for civil structures—built for precision, safety, and North America's B2B sector.{% endblock %}">
    <title>{% block title %}Civil Structure Test Tech{% endblock %}</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
        <div class="container">
            <a class="navbar-brand fw-bold" href="{{ url_for('index') }}">
                <i class="fas fa-building me-2"></i>Civil Structure Test Tech
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'index' %}active{% endif %}" href="{{ url_for('index') }}">
                            <i class="fas fa-home me-1"></i>Home
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'products' %}active{% endif %}" href="{{ url_for('products') }}">
                            <i class="fas fa-cogs me-1"></i>Products
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'services' %}active{% endif %}" href="{{ url_for('services') }}">
                            <i class="fas fa-tools me-1"></i>Services
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'about' %}active{% endif %}" href="{{ url_for('about') }}">
                            <i class="fas fa-info-circle me-1"></i>About
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'contact' %}active{% endif %}" href="{{ url_for('contact') }}">
                            <i class="fas fa-envelope me-1"></i>Contact
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Flash Messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <div class="flash-messages">
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'success' if category == 'success' else 'danger' }} alert-dismissible fade show" role="alert">
                        <i class="fas fa-{{ 'check-circle' if category == 'success' else 'exclamation-triangle' }} me-2"></i>
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}

    <!-- Main Content -->
    <main>
        {% if error_message %}
            <div class="container mt-5 pt-5">
                <div class="row justify-content-center">
                    <div class="col-lg-6 text-center">
                        <h2 class="text-primary">{{ error_message }}</h2>
                        <p class="text-muted">We apologize for the inconvenience.</p>
                        <a href="{{ url_for('index') }}" class="btn btn-primary">Return Home</a>
                    </div>
                </div>
            </div>
        {% else %}
            {% block content %}{% endblock %}
        {% endif %}
    </main>

    <!-- Footer -->
    <footer class="footer mt-5">
        <div class="container">
            <div class="row">
                <div class="col-lg-4">
                    <h5>Civil Structure Test Tech</h5>
                    <p class="text-light">Advanced testing equipment for safer civil structures across North America.</p>
                </div>
                <div class="col-lg-4">
                    <h6>Quick Links</h6>
                    <ul class="list-unstyled">
                        <li><a href="{{ url_for('products') }}" class="text-light">Products</a></li>
                        <li><a href="{{ url_for('services') }}" class="text-light">Services</a></li>
                        <li><a href="{{ url_for('about') }}" class="text-light">About Us</a></li>
                        <li><a href="{{ url_for('contact') }}" class="text-light">Contact</a></li>
                    </ul>
                </div>
                <div class="col-lg-4">
                    <h6>Contact Information</h6>
                    <p class="text-light mb-1"><i class="fas fa-map-marker-alt me-2"></i>Miami, FL</p>
                    <p class="text-light mb-1"><i class="fas fa-phone me-2"></i>Available upon request</p>
                    <p class="text-light mb-1"><i class="fas fa-envelope me-2"></i>Available upon request</p>
                </div>
            </div>
            <hr class="bg-light">
            <div class="row">
                <div class="col text-center">
                    <p class="mb-0 text-light">&copy; 2025 Civil Structure Test Tech. All rights reserved.</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap 5 JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Custom JS -->
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
{% extends "base.html" %}

{% block title %}Advanced Testing Equipment for Safer Civil Structures - Civil Structure Test Tech{% endblock %}

{% block content %}
<!-- Hero Section -->
<section class="hero">
    <div class="container">
        <div class="row align-items-center min-vh-100 pt-5">
            <div class="col-lg-6">
                <h1 class="display-4 fw-bold text-white mb-4">
                    Advanced Testing Equipment for Safer Civil Structures
                </h1>
                <p class="lead text-light mb-4">
                    Precision testing solutions for structural engineers, geotechnical professionals, and inspection teams across North America.
                </p>
                <div class="d-flex flex-wrap gap-3">
                    <a href="{{ url_for('products') }}" class="btn btn-light btn-lg">
                        <i class="fas fa-cogs me-2"></i>Explore Products
                    </a>
                    <a href="{{ url_for('services') }}" class="btn btn-outline-light btn-lg">
                        <i class="fas fa-tools me-2"></i>Get Quote
                    </a>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="hero-icon text-center">
                    <i class="fas fa-building fa-10x text-light opacity-75"></i>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Overview Section -->
<section class="py-5">
    <div class="container">
        <div class="row">
            <div class="col-lg-8 mx-auto text-center">
                <h2 class="display-5 fw-bold text-primary mb-4">Overview</h2>
                <p class="lead text-muted mb-4">
                    Civil infrastructure requires rigorous testing to ensure safety, durability, and long-term performance. 
                    We provide a full spectrum of specialized testing technologies tailored for structural engineers, 
                    geotechnical professionals, and inspection teams.
                </p>
                <p class="text-muted">
                    Serving a wide B2B market across North America, Civil Structure Test Tech delivers systems that 
                    meet the most demanding standards of performance, precision, and reliability. Based in Miami, FL, 
                    our team empowers clients with expert guidance, innovative research, and scalable solutions.
                </p>
            </div>
        </div>
    </div>
</section>

<!-- Key Features Section -->
<section class="py-5 bg-light">
    <div class="container">
        <div class="row">
            <div class="col text-center mb-5">
                <h2 class="display-5 fw-bold text-primary">Why Choose Our Solutions?</h2>
                <p class="lead text-muted">Industry-leading technology meets uncompromising quality</p>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-4 mb-4">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body text-center p-4">
                        <i class="fas fa-shield-alt fa-3x text-primary mb-3"></i>
                        <h5 class="card-title">Safety First</h5>
                        <p class="card-text text-muted">
                            All equipment meets the highest safety standards with comprehensive testing protocols.
                        </p>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body text-center p-4">
                        <i class="fas fa-accuracy fa-3x text-primary mb-3"></i>
                        <h5 class="card-title">Precision Engineering</h5>
                        <p class="card-text text-muted">
                            Advanced measurement systems deliver accurate, reliable results for critical applications.
                        </p>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body text-center p-4">
                        <i class="fas fa-users fa-3x text-primary mb-3"></i>
                        <h5 class="card-title">Expert Support</h5>
                        <p class="card-text text-muted">
                            Dedicated technical support and training from experienced engineers and specialists.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Equipment Categories Preview -->
<section class="py-5">
    <div class="container">
        <div class="row">
            <div class="col text-center mb-5">
                <h2 class="display-5 fw-bold text-primary">Core Testing Equipment Categories</h2>
                <p class="lead text-muted">Comprehensive solutions for every testing requirement</p>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0"><i class="fas fa-weight-hanging me-2"></i>Structural Load Testing</h5>
                    </div>
                    <div class="card-body">
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check text-success me-2"></i>Hydraulic Load Frames</li>
                            <li><i class="fas fa-check text-success me-2"></i>Actuator Systems</li>
                            <li><i class="fas fa-check text-success me-2"></i>Dynamic Shakers</li>
                            <li><i class="fas fa-check text-success me-2"></i>Prestress Force Measurement</li>
                        </ul>
                        <a href="{{ url_for('products') }}#structural" class="btn btn-outline-primary">Learn More</a>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0"><i class="fas fa-search me-2"></i>NDT & Sensing</h5>
                    </div>
                    <div class="card-body">
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check text-success me-2"></i>Digital Strain Gauge Systems</li>
                            <li><i class="fas fa-check text-success me-2"></i>Ultrasonic Testing</li>
                            <li><i class="fas fa-check text-success me-2"></i>Ground Penetrating Radar</li>
                            <li><i class="fas fa-check text-success me-2"></i>Infrared Thermography</li>
                        </ul>
                        <a href="{{ url_for('products') }}#ndt" class="btn btn-outline-primary">Learn More</a>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0"><i class="fas fa-layer-group me-2"></i>Geotechnical Testing</h5>
                    </div>
                    <div class="card-body">
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check text-success me-2"></i>Plate Load Test Systems</li>
                            <li><i class="fas fa-check text-success me-2"></i>Cone Penetrometer Testing</li>
                            <li><i class="fas fa-check text-success me-2"></i>Vane Shear Testers</li>
                            <li><i class="fas fa-check text-success me-2"></i>Pressuremeters</li>
                        </ul>
                        <a href="{{ url_for('products') }}#geotechnical" class="btn btn-outline-primary">Learn More</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Call to Action -->
<section class="py-5 bg-primary text-white">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-8">
                <h3 class="fw-bold mb-2">Ready to Enhance Your Testing Capabilities?</h3>
                <p class="lead mb-0">Contact our experts to discuss your specific testing requirements and get a custom quote.</p>
            </div>
            <div class="col-lg-4 text-lg-end">
                <a href="{{ url_for('contact') }}" class="btn btn-light btn-lg">
                    <i class="fas fa-envelope me-2"></i>Contact Us Today
                </a>
            </div>
        </div>
    </div>
</section>
{% endblock %}
{% extends "base.html" %}

{% block title %}Products - Testing Equipment Catalog - Civil Structure Test Tech{% endblock %}

{% block content %}
<section class="pt-5 mt-4">
    <div class="container">
        <div class="row">
            <div class="col text-center mb-5">
                <h1 class="display-4 fw-bold text-primary">Product Catalog</h1>
                <p class="lead text-muted">Comprehensive testing equipment for all your civil engineering needs</p>
            </div>
        </div>

        <!-- Structural Load & Response Testing -->
        <section id="structural" class="mb-5">
            <div class="row">
                <div class="col">
                    <h2 class="fw-bold text-primary mb-4">
                        <i class="fas fa-weight-hanging me-3"></i>Structural Load & Response Testing
                    </h2>
                </div>
            </div>
            <div class="row">
                <div class="col-lg-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">Hydraulic Load Frames</h5>
                            <p class="card-text text-muted">High-capacity testing frames for static and dynamic load applications.</p>
                            <ul class="list-unstyled">
                                <li><i class="fas fa-cog text-primary me-2"></i>Capacity: 50kN to 5000kN</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Precision: ±0.5% of reading</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Control: Digital servo-hydraulic</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Data: Real-time acquisition</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">Actuator Systems</h5>
                            <p class="card-text text-muted">Precision actuators for multi-axis testing and complex loading scenarios.</p>
                            <ul class="list-unstyled">
                                <li><i class="fas fa-cog text-primary me-2"></i>Force: Up to 2500kN</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Stroke: 100mm to 1000mm</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Frequency: 0.01 to 50 Hz</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Control: Multi-channel coordination</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">Static Load Testing Rigs</h5>
                            <p class="card-text text-muted">Customizable rigs for beam, column, and slab testing applications.</p>
                            <ul class="list-unstyled">
                                <li><i class="fas fa-cog text-primary me-2"></i>Configuration: Modular design</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Span: Up to 12 meters</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Loading: Point, distributed, cyclic</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Standards: ASTM, ISO, EN compliant</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">Dynamic Shakers & Vibration Tables</h5>
                            <p class="card-text text-muted">Seismic simulation and dynamic response testing equipment.</p>
                            <ul class="list-unstyled">
                                <li><i class="fas fa-cog text-primary me-2"></i>Force: 10N to 50kN</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Frequency: DC to 2000 Hz</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Acceleration: Up to 100g</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Control: Random, sine, shock</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- NDT & Sensing Tools -->
        <section id="ndt" class="mb-5">
            <div class="row">
                <div class="col">
                    <h2 class="fw-bold text-primary mb-4">
                        <i class="fas fa-search me-3"></i>Structural Sensing & NDT Tools
                    </h2>
                </div>
            </div>
            <div class="row">
                <div class="col-lg-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">Digital Strain Gauge Systems</h5>
                            <p class="card-text text-muted">High-precision strain measurement with wireless capabilities.</p>
                            <ul class="list-unstyled">
                                <li><i class="fas fa-cog text-primary me-2"></i>Resolution: 1 microstrain</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Channels: Up to 128 per unit</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Range: ±50,000 microstrain</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Sampling: Up to 10 kHz</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">Ultrasonic Pulse Velocity Testers</h5>
                            <p class="card-text text-muted">Non-destructive concrete quality assessment and defect detection.</p>
                            <ul class="list-unstyled">
                                <li><i class="fas fa-cog text-primary me-2"></i>Frequency: 54 kHz standard</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Resolution: 0.1 μs</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Range: 0.1 to 6553.5 μs</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Memory: 250 readings storage</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">Ground Penetrating Radar</h5>
                            <p class="card-text text-muted">Subsurface investigation and reinforcement detection systems.</p>
                            <ul class="list-unstyled">
                                <li><i class="fas fa-cog text-primary me-2"></i>Frequency: 100 MHz to 2.6 GHz</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Depth: Up to 3 meters in concrete</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Resolution: Sub-centimeter</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Display: Real-time imaging</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">Infrared Thermography Cameras</h5>
                            <p class="card-text text-muted">Thermal imaging for defect detection and energy audits.</p>
                            <ul class="list-unstyled">
                                <li><i class="fas fa-cog text-primary me-2"></i>Resolution: 640 x 480 pixels</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Temperature: -40°C to +1200°C</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Accuracy: ±2°C or ±2%</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Analysis: Advanced software suite</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Geotechnical & Foundation Testing -->
        <section id="geotechnical" class="mb-5">
            <div class="row">
                <div class="col">
                    <h2 class="fw-bold text-primary mb-4">
                        <i class="fas fa-layer-group me-3"></i>Geotechnical & Foundation Testing
                    </h2>
                </div>
            </div>
            <div class="row">
                <div class="col-lg-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">Plate Load Test Systems</h5>
                            <p class="card-text text-muted">In-situ bearing capacity and settlement testing equipment.</p>
                            <ul class="list-unstyled">
                                <li><i class="fas fa-cog text-primary me-2"></i>Plate sizes: 300mm to 762mm</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Load capacity: Up to 5000kN</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Settlement: 0.01mm resolution</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Standards: ASTM D1196, IS 1888</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">Piezocone Penetrometer Test</h5>
                            <p class="card-text text-muted">Advanced CPT systems for soil characterization and profiling.</p>
                            <ul class="list-unstyled">
                                <li><i class="fas fa-cog text-primary me-2"></i>Capacity: 200kN push force</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Depth: Up to 100 meters</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Parameters: qc, fs, u, inclination</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Rate: 20mm/second standard</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">Vane Shear Testers</h5>
                            <p class="card-text text-muted">In-situ shear strength measurement for cohesive soils.</p>
                            <ul class="list-unstyled">
                                <li><i class="fas fa-cog text-primary me-2"></i>Vane sizes: 33mm to 130mm</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Torque: Up to 980 N·m</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Rotation: 6°/minute standard</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Display: Digital readout</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">Pressuremeters</h5>
                            <p class="card-text text-muted">Lateral pressure testing for deformation modulus determination.</p>
                            <ul class="list-unstyled">
                                <li><i class="fas fa-cog text-primary me-2"></i>Pressure: Up to 5 MPa</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Volume: 535 cm³ capacity</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Depth: Up to 50 meters</li>
                                <li><i class="fas fa-cog text-primary me-2"></i>Control: Automatic pressure regulation</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Call to Action -->
        <section class="bg-primary text-white rounded p-5 text-center">
            <h3 class="fw-bold mb-3">Need Detailed Specifications or Custom Solutions?</h3>
            <p class="lead mb-4">Our technical team can provide detailed specifications, pricing, and custom configuration options for any equipment.</p>
            <div class="d-flex flex-wrap justify-content-center gap-3">
                <a href="{{ url_for('services') }}" class="btn btn-light btn-lg">
                    <i class="fas fa-clipboard-list me-2"></i>Request Quote
                </a>
                <a href="{{ url_for('contact') }}" class="btn btn-outline-light btn-lg">
                    <i class="fas fa-phone me-2"></i>Speak with Expert
                </a>
            </div>
        </section>
    </div>
</section>
{% endblock %}
{% extends "base.html" %}

{% block title %}Services - Testing Solutions & Support - Civil Structure Test Tech{% endblock %}

{% block content %}
<section class="pt-5 mt-4">
    <div class="container">
        <div class="row">
            <div class="col text-center mb-5">
                <h1 class="display-4 fw-bold text-primary">Our Services</h1>
                <p class="lead text-muted">Comprehensive testing solutions and expert support services</p>
            </div>
        </div>

        <!-- Service Categories -->
        <div class="row mb-5">
            <div class="col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-tools fa-3x text-primary mb-3"></i>
                        <h5 class="card-title">Equipment Installation & Setup</h5>
                        <p class="card-text text-muted">Professional installation, calibration, and commissioning of testing equipment at your facility.</p>
                        <ul class="list-unstyled text-start">
                            <li><i class="fas fa-check text-success me-2"></i>Site assessment and preparation</li>
                            <li><i class="fas fa-check text-success me-2"></i>Equipment installation and calibration</li>
                            <li><i class="fas fa-check text-success me-2"></i>System integration and testing</li>
                            <li><i class="fas fa-check text-success me-2"></i>Documentation and certification</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-graduation-cap fa-3x text-primary mb-3"></i>
                        <h5 class="card-title">Training & Certification</h5>
                        <p class="card-text text-muted">Comprehensive training programs to maximize your team's expertise and equipment utilization.</p>
                        <ul class="list-unstyled text-start">
                            <li><i class="fas fa-check text-success me-2"></i>Equipment operation training</li>
                            <li><i class="fas fa-check text-success me-2"></i>Safety protocols and procedures</li>
                            <li><i class="fas fa-check text-success me-2"></i>Data analysis and interpretation</li>
                            <li><i class="fas fa-check text-success me-2"></i>Certification programs available</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-wrench fa-3x text-primary mb-3"></i>
                        <h5 class="card-title">Maintenance & Support</h5>
                        <p class="card-text text-muted">Ongoing technical support and maintenance services to ensure optimal equipment performance.</p>
                        <ul class="list-unstyled text-start">
                            <li><i class="fas fa-check text-success me-2"></i>Preventive maintenance programs</li>
                            <li><i class="fas fa-check text-success me-2"></i>Emergency repair services</li>
                            <li><i class="fas fa-check text-success me-2"></i>Remote diagnostic support</li>
                            <li><i class="fas fa-check text-success me-2"></i>Spare parts and consumables</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mb-5">
            <div class="col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-clipboard-list fa-3x text-primary mb-3"></i>
                        <h5 class="card-title">Custom Testing Solutions</h5>
                        <p class="card-text text-muted">Tailored testing systems designed to meet your specific project requirements and constraints.</p>
                        <ul class="list-unstyled text-start">
                            <li><i class="fas fa-check text-success me-2"></i>Custom equipment design</li>
                            <li><i class="fas fa-check text-success me-2"></i>Specialized test procedures</li>
                            <li><i class="fas fa-check text-success me-2"></i>Integration with existing systems</li>
                            <li><i class="fas fa-check text-success me-2"></i>Prototype development</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-handshake fa-3x text-primary mb-3"></i>
                        <h5 class="card-title">Equipment Rental</h5>
                        <p class="card-text text-muted">Flexible rental options for short-term projects or equipment evaluation before purchase.</p>
                        <ul class="list-unstyled text-start">
                            <li><i class="fas fa-check text-success me-2"></i>Short-term and long-term rentals</li>
                            <li><i class="fas fa-check text-success me-2"></i>Rent-to-own options available</li>
                            <li><i class="fas fa-check text-success me-2"></i>Delivery and setup included</li>
                            <li><i class="fas fa-check text-success me-2"></i>Technical support during rental</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-user-tie fa-3x text-primary mb-3"></i>
                        <h5 class="card-title">Engineering Consultation</h5>
                        <p class="card-text text-muted">Expert consulting services for testing methodology, standard compliance, and result interpretation.</p>
                        <ul class="list-unstyled text-start">
                            <li><i class="fas fa-check text-success me-2"></i>Test method development</li>
                            <li><i class="fas fa-check text-success me-2"></i>Standards compliance review</li>
                            <li><i class="fas fa-check text-success me-2"></i>Data analysis and reporting</li>
                            <li><i class="fas fa-check text-success me-2"></i>Expert witness services</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <!-- Service Inquiry Form -->
        <section class="bg-light rounded p-5">
            <div class="row">
                <div class="col-lg-8 mx-auto">
                    <h2 class="text-center text-primary mb-4">Request Service Quote</h2>
                    <p class="text-center text-muted mb-4">
                        Tell us about your project requirements and our team will provide you with a detailed service proposal.
                    </p>
                    
                    <form method="POST" action="{{ url_for('services_post') }}">
                        {{ form.hidden_tag() }}
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                {{ form.company.label(class="form-label") }}
                                {{ form.company(class="form-control") }}
                                {% if form.company.errors %}
                                    <div class="text-danger small">
                                        {% for error in form.company.errors %}
                                            <div>{{ error }}</div>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                            <div class="col-md-6 mb-3">
                                {{ form.name.label(class="form-label") }}
                                {{ form.name(class="form-control") }}
                                {% if form.name.errors %}
                                    <div class="text-danger small">
                                        {% for error in form.name.errors %}
                                            <div>{{ error }}</div>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                {{ form.email.label(class="form-label") }}
                                {{ form.email(class="form-control") }}
                                {% if form.email.errors %}
                                    <div class="text-danger small">
                                        {% for error in form.email.errors %}
                                            <div>{{ error }}</div>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                            <div class="col-md-6 mb-3">
                                {{ form.phone.label(class="form-label") }}
                                {{ form.phone(class="form-control") }}
                                {% if form.phone.errors %}
                                    <div class="text-danger small">
                                        {% for error in form.phone.errors %}
                                            <div>{{ error }}</div>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            {{ form.service_type.label(class="form-label") }}
                            {{ form.service_type(class="form-select") }}
                            {% if form.service_type.errors %}
                                <div class="text-danger small">
                                    {% for error in form.service_type.errors %}
                                        <div>{{ error }}</div>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-4">
                            {{ form.project_details.label(class="form-label") }}
                            {{ form.project_details(class="form-control", rows="6", placeholder="Please describe your project requirements, timeline, location, and any specific testing needs...") }}
                            {% if form.project_details.errors %}
                                <div class="text-danger small">
                                    {% for error in form.project_details.errors %}
                                        <div>{{ error }}</div>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="text-center">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-paper-plane me-2"></i>Submit Service Request
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </section>

        <!-- Support Information -->
        <section class="mt-5">
            <div class="row">
                <div class="col text-center">
                    <h3 class="text-primary mb-4">Need Immediate Support?</h3>
                    <div class="row">
                        <div class="col-lg-4">
                            <i class="fas fa-phone fa-2x text-primary mb-2"></i>
                            <h6>Emergency Support</h6>
                            <p class="text-muted">24/7 technical support for critical equipment issues</p>
                        </div>
                        <div class="col-lg-4">
                            <i class="fas fa-envelope fa-2x text-primary mb-2"></i>
                            <h6>Technical Questions</h6>
                            <p class="text-muted">Expert guidance on testing procedures and methodologies</p>
                        </div>
                        <div class="col-lg-4">
                            <i class="fas fa-clock fa-2x text-primary mb-2"></i>
                            <h6>Response Time</h6>
                            <p class="text-muted">Same-day response for all service inquiries</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</section>
{% endblock %}
{% extends "base.html" %}

{% block title %}About Us - Company Information & Team - Civil Structure Test Tech{% endblock %}

{% block content %}
<section class="pt-5 mt-4">
    <div class="container">
        <!-- Company Overview -->
        <div class="row mb-5">
            <div class="col text-center">
                <h1 class="display-4 fw-bold text-primary mb-4">About Civil Structure Test Tech</h1>
                <p class="lead text-muted">Leading provider of advanced testing equipment for civil engineering professionals across North America</p>
            </div>
        </div>

        <!-- Mission & Vision -->
        <div class="row mb-5">
            <div class="col-lg-6 mb-4">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body p-4">
                        <i class="fas fa-bullseye fa-3x text-primary mb-3"></i>
                        <h3 class="card-title text-primary">Our Mission</h3>
                        <p class="card-text">
                            To empower civil engineers, structural professionals, and testing laboratories with cutting-edge 
                            equipment and expertise that ensures the safety, reliability, and longevity of critical infrastructure.
                        </p>
                        <p class="card-text">
                            We are committed to advancing the field of structural testing through innovative technology, 
                            exceptional service, and unwavering dedication to quality and precision.
                        </p>
                    </div>
                </div>
            </div>
            <div class="col-lg-6 mb-4">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body p-4">
                        <i class="fas fa-eye fa-3x text-primary mb-3"></i>
                        <h3 class="card-title text-primary">Our Vision</h3>
                        <p class="card-text">
                            To be North America's most trusted partner in civil structure testing, recognized for our 
                            innovative solutions, technical excellence, and contribution to safer, more resilient infrastructure.
                        </p>
                        <p class="card-text">
                            We envision a future where advanced testing technologies enable engineers to build with 
                            unprecedented confidence and precision, protecting communities and advancing society.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Company History & Values -->
        <div class="row mb-5">
            <div class="col-lg-8 mx-auto">
                <h2 class="text-center text-primary mb-4">Our Story</h2>
                <p class="text-muted">
                    Founded in Miami, Florida, Civil Structure Test Tech emerged from a recognition that the civil 
                    engineering industry needed more sophisticated, reliable, and accessible testing equipment. Our 
                    founders, experienced engineers and industry professionals, understood the critical role that 
                    precise testing plays in ensuring structural safety and performance.
                </p>
                <p class="text-muted">
                    Starting with a focus on the B2B market across North America, we have built our reputation on 
                    delivering not just equipment, but complete testing solutions. Our approach combines state-of-the-art 
                    technology with deep industry knowledge, providing clients with the tools and support they need 
                    to meet the most demanding testing requirements.
                </p>
                <p class="text-muted">
                    Today, we continue to innovate and expand our offerings, staying at the forefront of testing 
                    technology while maintaining our commitment to exceptional service and technical excellence.
                </p>
            </div>
        </div>

        <!-- Core Values -->
        <div class="row mb-5">
            <div class="col text-center mb-4">
                <h2 class="text-primary">Our Core Values</h2>
            </div>
        </div>
        <div class="row mb-5">
            <div class="col-lg-3 col-md-6 mb-4">
                <div class="text-center">
                    <i class="fas fa-shield-alt fa-3x text-primary mb-3"></i>
                    <h5 class="text-primary">Safety First</h5>
                    <p class="text-muted">
                        Every product and service we provide prioritizes the safety of people and structures, 
                        meeting the highest industry standards.
                    </p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 mb-4">
                <div class="text-center">
                    <i class="fas fa-award fa-3x text-primary mb-3"></i>
                    <h5 class="text-primary">Excellence</h5>
                    <p class="text-muted">
                        We strive for excellence in everything we do, from product quality to customer service 
                        and technical support.
                    </p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 mb-4">
                <div class="text-center">
                    <i class="fas fa-lightbulb fa-3x text-primary mb-3"></i>
                    <h5 class="text-primary">Innovation</h5>
                    <p class="text-muted">
                        Continuous innovation drives our development of new technologies and solutions that 
                        advance the testing industry.
                    </p>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 mb-4">
                <div class="text-center">
                    <i class="fas fa-handshake fa-3x text-primary mb-3"></i>
                    <h5 class="text-primary">Partnership</h5>
                    <p class="text-muted">
                        We build lasting partnerships with our clients, providing ongoing support and expertise 
                        for their success.
                    </p>
                </div>
            </div>
        </div>

        <!-- Team Section -->
        <div class="row mb-5">
            <div class="col text-center mb-4">
                <h2 class="text-primary">Our Expert Team</h2>
                <p class="lead text-muted">Experienced professionals dedicated to your testing success</p>
            </div>
        </div>
        <div class="row mb-5">
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card h-100 border-0 shadow-sm text-center">
                    <div class="card-body p-4">
                        <div class="avatar-placeholder bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
                            <i class="fas fa-user fa-2x"></i>
                        </div>
                        <h5 class="card-title">Engineering Team</h5>
                        <p class="text-muted mb-2">Structural & Geotechnical Engineers</p>
                        <p class="card-text small">
                            Our team of licensed professional engineers brings decades of combined experience 
                            in structural testing, geotechnical analysis, and equipment design.
                        </p>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card h-100 border-0 shadow-sm text-center">
                    <div class="card-body p-4">
                        <div class="avatar-placeholder bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
                            <i class="fas fa-cogs fa-2x"></i>
                        </div>
                        <h5 class="card-title">Technical Support</h5>
                        <p class="text-muted mb-2">Equipment Specialists</p>
                        <p class="card-text small">
                            Certified technicians and equipment specialists provide comprehensive training, 
                            installation, and ongoing support for all our testing systems.
                        </p>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card h-100 border-0 shadow-sm text-center">
                    <div class="card-body p-4">
                        <div class="avatar-placeholder bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
                            <i class="fas fa-chart-line fa-2x"></i>
                        </div>
                        <h5 class="card-title">Sales & Consulting</h5>
                        <p class="text-muted mb-2">Solution Specialists</p>
                        <p class="card-text small">
                            Experienced consultants who understand your testing challenges and work with you 
                            to develop customized solutions that meet your specific requirements.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Certifications & Standards -->
        <div class="row mb-5">
            <div class="col-lg-8 mx-auto">
                <h2 class="text-center text-primary mb-4">Certifications & Standards</h2>
                <p class="text-center text-muted mb-4">
                    Our equipment and processes meet or exceed industry standards and regulatory requirements.
                </p>
                <div class="row text-center">
                    <div class="col-md-3 mb-3">
                        <i class="fas fa-certificate fa-2x text-primary mb-2"></i>
                        <h6>ASTM Compliant</h6>
                        <p class="small text-muted">All testing equipment meets ASTM standards</p>
                    </div>
                    <div class="col-md-3 mb-3">
                        <i class="fas fa-globe fa-2x text-primary mb-2"></i>
                        <h6>ISO Certified</h6>
                        <p class="small text-muted">Quality management systems certified</p>
                    </div>
                    <div class="col-md-3 mb-3">
                        <i class="fas fa-check-circle fa-2x text-primary mb-2"></i>
                        <h6>EN Standards</h6>
                        <p class="small text-muted">European standard compliance available</p>
                    </div>
                    <div class="col-md-3 mb-3">
                        <i class="fas fa-shield-alt fa-2x text-primary mb-2"></i>
                        <h6>Safety Certified</h6>
                        <p class="small text-muted">Comprehensive safety testing and certification</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Call to Action -->
        <section class="bg-primary text-white rounded p-5 text-center">
            <h3 class="fw-bold mb-3">Ready to Work with the Experts?</h3>
            <p class="lead mb-4">
                Let our experienced team help you find the perfect testing solution for your project requirements.
            </p>
            <div class="d-flex flex-wrap justify-content-center gap-3">
                <a href="{{ url_for('contact') }}" class="btn btn-light btn-lg">
                    <i class="fas fa-envelope me-2"></i>Contact Our Team
                </a>
                <a href="{{ url_for('services') }}" class="btn btn-outline-light btn-lg">
                    <i class="fas fa-clipboard-list me-2"></i>Request Consultation
                </a>
            </div>
        </section>
    </div>
</section>
{% endblock %}
{% extends "base.html" %}

{% block title %}Contact Us - Get in Touch - Civil Structure Test Tech{% endblock %}

{% block content %}
<section class="pt-5 mt-4">
    <div class="container">
        <div class="row">
            <div class="col text-center mb-5">
                <h1 class="display-4 fw-bold text-primary">Contact Us</h1>
                <p class="lead text-muted">Get in touch with our team for expert assistance with your testing needs</p>
            </div>
        </div>

        <div class="row">
            <!-- Contact Information -->
            <div class="col-lg-4 mb-5">
                <div class="card h-100 border-0 shadow-sm">
                    <div class="card-body p-4">
                        <h3 class="text-primary mb-4">Get in Touch</h3>
                        
                        <div class="contact-item mb-4">
                            <div class="d-flex align-items-start">
                                <i class="fas fa-map-marker-alt fa-lg text-primary me-3 mt-1"></i>
                                <div>
                                    <h6 class="mb-1">Our Location</h6>
                                    <p class="text-muted mb-0">
                                        Miami, FL<br>
                                        United States
                                    </p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="contact-item mb-4">
                            <div class="d-flex align-items-start">
                                <i class="fas fa-phone fa-lg text-primary me-3 mt-1"></i>
                                <div>
                                    <h6 class="mb-1">Phone Support</h6>
                                    <p class="text-muted mb-0">
                                        Available upon request<br>
                                        <small>Business Hours: Mon-Fri 8AM-6PM EST</small>
                                    </p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="contact-item mb-4">
                            <div class="d-flex align-items-start">
                                <i class="fas fa-envelope fa-lg text-primary me-3 mt-1"></i>
                                <div>
                                    <h6 class="mb-1">Email</h6>
                                    <p class="text-muted mb-0">
                                        Contact form preferred<br>
                                        <small>We respond within 24 hours</small>
                                    </p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="contact-item">
                            <div class="d-flex align-items-start">
                                <i class="fas fa-clock fa-lg text-primary me-3 mt-1"></i>
                                <div>
                                    <h6 class="mb-1">Response Time</h6>
                                    <p class="text-muted mb-0">
                                        Same-day response<br>
                                        <small>Emergency support available 24/7</small>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Contact Form -->
            <div class="col-lg-8">
                <div class="card border-0 shadow-sm">
                    <div class="card-body p-5">
                        <h3 class="text-primary mb-4">Send us a Message</h3>
                        <p class="text-muted mb-4">
                            Have questions about our products or need technical assistance? Fill out the form below 
                            and our team will get back to you promptly.
                        </p>
                        
                        <form method="POST" action="{{ url_for('contact_post') }}">
                            {{ form.hidden_tag() }}
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    {{ form.name.label(class="form-label") }}
                                    {{ form.name(class="form-control form-control-lg") }}
                                    {% if form.name.errors %}
                                        <div class="text-danger small mt-1">
                                            {% for error in form.name.errors %}
                                                <div>{{ error }}</div>
                                            {% endfor %}
                                        </div>
                                    {% endif %}
                                </div>
                                <div class="col-md-6 mb-3">
                                    {{ form.email.label(class="form-label") }}
                                    {{ form.email(class="form-control form-control-lg") }}
                                    {% if form.email.errors %}
                                        <div class="text-danger small mt-1">
                                            {% for error in form.email.errors %}
                                                <div>{{ error }}</div>
                                            {% endfor %}
                                        </div>
                                    {% endif %}
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                {{ form.subject.label(class="form-label") }}
                                {{ form.subject(class="form-control form-control-lg") }}
                                {% if form.subject.errors %}
                                    <div class="text-danger small mt-1">
                                        {% for error in form.subject.errors %}
                                            <div>{{ error }}</div>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                            
                            <div class="mb-4">
                                {{ form.message.label(class="form-label") }}
                                {{ form.message(class="form-control", rows="6", placeholder="Please describe your inquiry, testing requirements, or any questions you have about our products and services...") }}
                                {% if form.message.errors %}
                                    <div class="text-danger small mt-1">
                                        {% for error in form.message.errors %}
                                            <div>{{ error }}</div>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                            
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="fas fa-paper-plane me-2"></i>Send Message
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <!-- Additional Support Options -->
        <div class="row mt-5">
            <div class="col text-center">
                <h3 class="text-primary mb-4">Other Ways to Reach Us</h3>
            </div>
        </div>
        <div class="row mb-5">
            <div class="col-lg-4 mb-4">
                <div class="card text-center border-0 shadow-sm h-100">
                    <div class="card-body p-4">
                        <i class="fas fa-question-circle fa-3x text-primary mb-3"></i>
                        <h5 class="card-title">Technical Questions</h5>
                        <p class="card-text text-muted">
                            Need help with equipment specifications, testing procedures, or technical documentation?
                        </p>
                        <a href="{{ url_for('services') }}" class="btn btn-outline-primary">
                            Technical Support
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="card text-center border-0 shadow-sm h-100">
                    <div class="card-body p-4">
                        <i class="fas fa-calculator fa-3x text-primary mb-3"></i>
                        <h5 class="card-title">Request Quote</h5>
                        <p class="card-text text-muted">
                            Looking for pricing information or custom solution quotes? Use our specialized quote form.
                        </p>
                        <a href="{{ url_for('services') }}" class="btn btn-outline-primary">
                            Get Quote
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="card text-center border-0 shadow-sm h-100">
                    <div class="card-body p-4">
                        <i class="fas fa-exclamation-triangle fa-3x text-primary mb-3"></i>
                        <h5 class="card-title">Emergency Support</h5>
                        <p class="card-text text-muted">
                            Critical equipment issues that need immediate attention? We provide 24/7 emergency support.
                        </p>
                        <p class="text-primary mb-0">
                            <strong>Call available upon contact</strong>
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Service Areas -->
        <section class="bg-light rounded p-5">
            <div class="row">
                <div class="col text-center mb-4">
                    <h3 class="text-primary">Service Areas</h3>
                    <p class="text-muted">We proudly serve clients throughout North America</p>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4 text-center mb-3">
                    <i class="fas fa-map-marked-alt fa-2x text-primary mb-2"></i>
                    <h6>United States</h6>
                    <p class="text-muted small">All 50 states with specialized support in major metropolitan areas</p>
                </div>
                <div class="col-md-4 text-center mb-3">
                    <i class="fas fa-maple-leaf fa-2x text-primary mb-2"></i>
                    <h6>Canada</h6>
                    <p class="text-muted small">Full service coverage across all Canadian provinces</p>
                </div>
                <div class="col-md-4 text-center mb-3">
                    <i class="fas fa-globe-americas fa-2x text-primary mb-2"></i>
                    <h6>Mexico</h6>
                    <p class="text-muted small">Growing presence in major industrial centers</p>
                </div>
            </div>
        </section>
    </div>
</section>
{% endblock %}
/* Custom styles for Civil Structure Test Tech */

:root {
    --primary-color: #003366;
    --primary-dark: #002244;
    --primary-light: #004488;
    --text-light: #f8f9fa;
    --text-muted: #6c757d;
    --shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    --shadow-lg: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

/* Base styles */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    padding-top: 76px; /* Account for fixed navbar */
}

/* Navigation styles */
.navbar {
    background: var(--primary-color) !important;
    box-shadow: var(--shadow-lg);
    transition: all 0.3s ease;
}

.navbar-brand {
    font-size: 1.5rem;
    font-weight: 700;
}

.navbar-nav .nav-link {
    font-weight: 500;
    padding: 0.5rem 1rem !important;
    transition: all 0.3s ease;
    position: relative;
}

.navbar-nav .nav-link:hover {
    color: #ffffff !important;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 0.375rem;
}

.navbar-nav .nav-link.active {
    color: #ffffff !important;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 0.375rem;
}

/* Hero section */
.hero {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
    opacity: 0.3;
}

.hero .container {
    position: relative;
    z-index: 1;
}

.hero-icon {
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

/* Cards and components */
.card {
    transition: all 0.3s ease;
    border: none;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}

.card-header {
    border: none;
    font-weight: 600;
}

/* Buttons */
.btn {
    font-weight: 500;
    border-radius: 0.5rem;
    padding: 0.5rem 1.5rem;
    transition: all 0.3s ease;
    border: none;
}

.btn-primary {
    background: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background: var(--primary-dark);
    color: white;
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.btn-outline-primary {
    border: 2px solid var(--primary-color);
    color: var(--primary-color);
}

.btn-outline-primary:hover {
    background: var(--primary-color);
    border-color: var(--primary-color);
    color: white;
    transform: translateY(-2px);
}

.btn-light {
    background: white;
    color: var(--primary-color);
}

.btn-light:hover {
    background: #f8f9fa;
    color: var(--primary-dark);
    transform: translateY(-2px);
}

.btn-outline-light:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: white;
    color: white;
}

/* Forms */
.form-control, .form-select {
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    padding: 0.75rem;
    transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 0.2rem rgba(0, 51, 102, 0.25);
}

.form-label {
    font-weight: 500;
    color: #333;
    margin-bottom: 0.5rem;
}

/* Flash messages */
.flash-messages {
    position: fixed;
    top: 76px;
    left: 0;
    right: 0;
    z-index: 1050;
    padding: 1rem;
    max-width: 600px;
    margin: 0 auto;
}

.flash-messages .alert {
    margin-bottom: 0.5rem;
    border: none;
    border-radius: 0.5rem;
    box-shadow: var(--shadow-lg);
}

/* Footer */
.footer {
    background: var(--primary-color);
    color: var(--text-light);
    padding: 3rem 0 1rem;
}

.footer h5, .footer h6 {
    color: white;
    font-weight: 600;
}

.footer a {
    color: var(--text-light);
    text-decoration: none;
    transition: all 0.3s ease;
}

.footer a:hover {
    color: white;
    text-decoration: underline;
}

/* Utility classes */
.text-primary {
    color: var(--primary-color) !important;
}

.bg-primary {
    background-color: var(--primary-color) !important;
}

/* Contact page specific styles */
.contact-item {
    padding: 1rem 0;
    border-bottom: 1px solid #eee;
}

.contact-item:last-child {
    border-bottom: none;
}

/* Avatar placeholder */
.avatar-placeholder {
    font-size: 1.5rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    body {
        padding-top: 66px;
    }
    
    .hero .display-4 {
        font-size: 2rem;
    }
    
    .navbar-brand {
        font-size: 1.2rem;
    }
    
    .hero-icon {
        margin-top: 2rem;
    }
    
    .hero-icon i {
        font-size: 4rem !important;
    }
    
    .card-body {
        padding: 1.5rem !important;
    }
}

@media (max-width: 576px) {
    .hero .display-4 {
        font-size: 1.75rem;
    }
    
    .btn-lg {
        padding: 0.5rem 1rem;
        font-size: 1rem;
    }
    
    .hero-icon i {
        font-size: 3rem !important;
    }
}

/* Animation classes */
.fade-in {
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Loading states */
.btn.loading {
    pointer-events: none;
    opacity: 0.6;
}

.btn.loading::after {
    content: '';
    width: 16px;
    height: 16px;
    margin-left: 8px;
    border: 2px solid transparent;
    border-top: 2px solid currentColor;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    display: inline-block;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Print styles */
@media print {
    .navbar, .footer, .btn {
        display: none !important;
    }
    
    body {
        padding-top: 0;
        color: black;
    }
    
    .hero {
        background: none !important;
        color: black !important;
    }
}
// Main JavaScript for Civil Structure Test Tech website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initSmoothScrolling();
    initFormValidation();
    initLoadingStates();
    initAnimations();
    initTooltips();
});

// Smooth scrolling for anchor links
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80; // Account for fixed navbar
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Enhanced form validation and UX
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                // Clear error state when user starts typing
                if (this.classList.contains('is-invalid')) {
                    this.classList.remove('is-invalid');
                    const errorMsg = this.parentNode.querySelector('.text-danger');
                    if (errorMsg) {
                        errorMsg.style.display = 'none';
                    }
                }
            });
        });
        
        // Form submission handling
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (isValid) {
                showLoadingState(form);
            }
        });
    });
}

// Field validation function
function validateField(field) {
    const value = field.value.trim();
    const isRequired = field.hasAttribute('required');
    const fieldType = field.type;
    let isValid = true;
    
    // Remove previous validation state
    field.classList.remove('is-valid', 'is-invalid');
    
    // Check if required field is empty
    if (isRequired && value === '') {
        showFieldError(field, 'This field is required');
        return false;
    }
    
    // Email validation
    if (fieldType === 'email' && value !== '') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showFieldError(field, 'Please enter a valid email address');
            return false;
        }
    }
    
    // Phone validation
    if (fieldType === 'tel' && value !== '') {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        if (!phoneRegex.test(value.replace(/[\s\-\(\)]/g, ''))) {
            showFieldError(field, 'Please enter a valid phone number');
            return false;
        }
    }
    
    // Text length validation
    if (field.hasAttribute('minlength')) {
        const minLength = parseInt(field.getAttribute('minlength'));
        if (value.length < minLength) {
            showFieldError(field, `Minimum ${minLength} characters required`);
            return false;
        }
    }
    
    if (isValid && value !== '') {
        field.classList.add('is-valid');
    }
    
    return isValid;
}

// Show field error
function showFieldError(field, message) {
    field.classList.add('is-invalid');
    
    let errorDiv = field.parentNode.querySelector('.field-error');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'field-error text-danger small mt-1';
        field.parentNode.appendChild(errorDiv);
    }
    
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

// Loading states for forms
function initLoadingStates() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            showLoadingState(form);
        });
    });
}

function showLoadingState(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (submitBtn) {
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = submitBtn.innerHTML.replace(/<i[^>]*><\/i>/, '<i class="fas fa-spinner fa-spin"></i>');
        
        // Reset after 30 seconds (safety fallback)
        setTimeout(() => {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }, 30000);
    }
}

// Scroll-based animations
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animatedElements = document.querySelectorAll('.card, .hero, section');
    animatedElements.forEach(el => observer.observe(el));
}

// Initialize tooltips
function initTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Auto-dismiss alerts after 5 seconds
function initAutoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentNode) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-20px)';
                
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }
        }, 5000);
    });
}

// Call auto-dismiss on page load
document.addEventListener('DOMContentLoaded', initAutoDismissAlerts);

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(0, 51, 102, 0.95)';
        navbar.style.backdropFilter = 'blur(10px)';
    } else {
        navbar.style.background = 'var(--primary-color)';
        navbar.style.backdropFilter = 'none';
    }
});

// Utility functions
const Utils = {
    // Debounce function for performance optimization
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    },
    
    // Format phone numbers
    formatPhone: function(phoneNumber) {
        const cleaned = phoneNumber.replace(/\D/g, '');
        const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
        if (match) {
            return '(' + match[1] + ') ' + match[2] + '-' + match[3];
        }
        return phoneNumber;
    },
    
    // Validate email format
    isValidEmail: function(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
};

// Export utility functions for global use
window.CSTTUtils = Utils;

// Service worker registration (if available)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Service worker could be added here for offline functionality
        console.log('Service Worker support detected');
    });
}

// Error handling for uncaught errors
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // Could send error reports to logging service
});

// Console welcome message
console.log(`
%c Civil Structure Test Tech %c
Advanced Testing Equipment for Safer Civil Structures
Visit our website: Built with Flask & Bootstrap 5
`, 
'color: white; background: #003366; padding: 10px; font-size: 16px; font-weight: bold;',
'color: #003366; font-size: 14px; padding: 10px;'
);
