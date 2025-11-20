# TODO: Add Online Payment Workflow and UI Improvements

## Phase 1: Database and Config Updates
- [ ] Update config.py to add UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH
- [ ] Update requirements.txt to add Flask-WTF file validators (FileAllowed, FileSize)
- [ ] Create models/settings_service.py for managing site settings (QR code URL)
- [ ] Update OrderService to handle new payment fields (payment_method, payment_status, payment_screenshot_url, etc.)
- [ ] Update seed.py to add initial QR code setting

## Phase 2: Forms and Validation
- [ ] Update CheckoutForm in blueprints/user/forms.py to include payment_method, confirm_payment, payment_screenshot
- [ ] Add PaymentQRForm in blueprints/admin/forms.py for QR upload
- [ ] Add PaymentVerifyForm in blueprints/admin/forms.py for admin verification

## Phase 3: Backend Routes
- [ ] Update checkout route in blueprints/user/routes.py to handle payment logic
- [ ] Add /api/upload_screenshot route for AJAX screenshot upload
- [ ] Add admin routes for QR management (/admin/payment-qr)
- [ ] Add admin routes for payment verification (/admin/orders/<id>/payment)
- [ ] Update order creation to include payment fields

## Phase 4: Templates and UI
- [ ] Create templates/user/checkout.html with Tailwind, payment options, QR display
- [ ] Update templates/layouts/base.html to use Tailwind CDN instead of Bootstrap
- [ ] Update templates/layouts/admin_base.html to use Tailwind
- [ ] Update templates/admin/orders_list.html to show payment status
- [ ] Update templates/admin/order_detail.html to show payment info and verification
- [ ] Update templates/user/order_detail.html to show payment status
- [ ] Add modal for screenshot preview

## Phase 5: File Handling
- [ ] Create static/uploads/ directory
- [ ] Add file upload utilities (secure_filename, unique naming)
- [ ] Add cloud storage support (optional, configurable)

## Phase 6: Testing
- [ ] Add unit tests for OrderService payment methods
- [ ] Add integration tests for checkout flow
- [ ] Add tests for file upload validation
- [ ] Add tests for admin verification

## Phase 7: Final Touches
- [ ] Update all templates to responsive Tailwind design
- [ ] Add toast notifications for success/error
- [ ] Ensure CSRF protection on all forms
- [ ] Test backwards compatibility
