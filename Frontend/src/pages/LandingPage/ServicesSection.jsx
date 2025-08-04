import React from 'react';
import { motion } from 'framer-motion';
import { Truck, FileCheck, Bell, Package, Shield, Clock } from 'lucide-react';
import Card from '../../components/Card';

const ServicesSection = () => {
  const services = [
    {
      icon: Truck,
      title: 'International Delivery',
      description: 'Fast and reliable shipping to over 200 countries with real-time tracking and insurance coverage.',
      features: ['Door-to-door delivery', 'Real-time tracking', 'Insurance included', 'Express options']
    },
    {
      icon: FileCheck,
      title: 'Customs Clearance',
      description: 'Expert handling of all customs documentation and procedures to ensure smooth border crossings.',
      features: ['Documentation assistance', 'Duty calculation', 'Compliance check', 'Fast processing']
    },
    {
      icon: Bell,
      title: 'Smart Notifications',
      description: 'Stay informed with instant updates about your shipment status via SMS, email, and app notifications.',
      features: ['SMS alerts', 'Email updates', 'Push notifications', 'Delivery confirmations']
    }
  ];

  const additionalServices = [
    { icon: Package, title: 'Package Consolidation', description: 'Combine multiple orders to save on shipping costs' },
    { icon: Shield, title: 'Insurance Coverage', description: 'Comprehensive protection for your valuable items' },
    { icon: Clock, title: '24/7 Support', description: 'Round-the-clock customer service and assistance' }
  ];

  return (
    <section id="services" className="py-20 bg-white dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Our Services
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            Comprehensive logistics solutions designed to meet all your international shipping needs
          </p>
        </motion.div>

        {/* Main Services */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          {services.map((service, index) => (
            <motion.div
              key={service.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: index * 0.2 }}
              viewport={{ once: true }}
            >
              <Card className="p-8 h-full text-center">
                <div className="bg-blue-100 dark:bg-blue-900 p-4 rounded-full w-16 h-16 mx-auto mb-6">
                  <service.icon className="w-8 h-8 text-blue-600 dark:text-blue-400 mx-auto mt-2" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                  {service.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 mb-6">
                  {service.description}
                </p>
                <ul className="space-y-2">
                  {service.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="text-sm text-gray-500 dark:text-gray-400 flex items-center">
                      <div className="w-1.5 h-1.5 bg-blue-600 rounded-full mr-2" />
                      {feature}
                    </li>
                  ))}
                </ul>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Additional Services */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="grid grid-cols-1 md:grid-cols-3 gap-8"
        >
          {additionalServices.map((service, index) => (
            <Card key={service.title} className="p-6 text-center">
              <div className="bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-800 dark:to-gray-700 p-3 rounded-lg w-12 h-12 mx-auto mb-4">
                <service.icon className="w-6 h-6 text-blue-600 dark:text-blue-400 mx-auto" />
              </div>
              <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                {service.title}
              </h4>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {service.description}
              </p>
            </Card>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default ServicesSection;