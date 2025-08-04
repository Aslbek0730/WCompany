import React from 'react';
import { Truck, Mail, Phone, MapPin } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="bg-blue-600 p-2 rounded-lg">
                <Truck className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold">WorldCompany</span>
            </div>
            <p className="text-gray-400 mb-4">
              Your trusted partner for international cargo and mail management. 
              Safe, secure, and reliable delivery services worldwide.
            </p>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <Mail size={16} className="text-blue-400" />
                <span className="text-gray-400">support@worldcompany.com</span>
              </div>
              <div className="flex items-center space-x-2">
                <Phone size={16} className="text-blue-400" />
                <span className="text-gray-400">+1 (555) 123-4567</span>
              </div>
              <div className="flex items-center space-x-2">
                <MapPin size={16} className="text-blue-400" />
                <span className="text-gray-400">123 Business Ave, City, Country</span>
              </div>
            </div>
          </div>

          {/* Services */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Services</h3>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">International Shipping</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Customs Clearance</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Package Tracking</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Express Delivery</a></li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Support</h3>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Help Center</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Contact Us</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Terms of Service</a></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center">
          <p className="text-gray-400">
            © 2024 WorldCompany. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;