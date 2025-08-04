import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Shield, Globe, Zap } from 'lucide-react';
import { Link } from 'react-router-dom';
import Button from '../../components/Button';

const HeroSection = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      {/* Animated Background Elements */}
      <div className="absolute inset-0">
        <motion.div
          className="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-70"
          animate={{
            x: [0, 50, 0],
            y: [0, -50, 0],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "linear"
          }}
        />
        <motion.div
          className="absolute top-1/3 right-1/4 w-72 h-72 bg-purple-400 rounded-full mix-blend-multiply filter blur-xl opacity-70"
          animate={{
            x: [0, -50, 0],
            y: [0, 50, 0],
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            ease: "linear"
          }}
        />
        <motion.div
          className="absolute bottom-1/4 left-1/3 w-72 h-72 bg-pink-400 rounded-full mix-blend-multiply filter blur-xl opacity-70"
          animate={{
            x: [0, 30, 0],
            y: [0, -30, 0],
          }}
          transition={{
            duration: 15,
            repeat: Infinity,
            ease: "linear"
          }}
        />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-gray-900 dark:text-white mb-6">
            Your International Cargo is{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
              Safe with Us!
            </span>
          </h1>
        </motion.div>

        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto"
        >
          Experience seamless international shipping with real-time tracking, 
          customs handling, and secure delivery to anywhere in the world.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12"
        >
          <Link to="/register">
            <Button size="xl" className="group">
              Get Started Today
              <ArrowRight size={20} className="ml-2 group-hover:translate-x-1 transition-transform" />
            </Button>
          </Link>
          <Button variant="outline" size="xl">
            Track Your Package
          </Button>
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto"
        >
          <div className="text-center">
            <div className="bg-white dark:bg-gray-800 p-4 rounded-full w-16 h-16 mx-auto mb-4 shadow-lg">
              <Shield className="w-8 h-8 text-blue-600 mx-auto mt-2" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Secure & Safe</h3>
            <p className="text-gray-600 dark:text-gray-400">End-to-end security for all your shipments</p>
          </div>
          <div className="text-center">
            <div className="bg-white dark:bg-gray-800 p-4 rounded-full w-16 h-16 mx-auto mb-4 shadow-lg">
              <Globe className="w-8 h-8 text-blue-600 mx-auto mt-2" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Global Reach</h3>
            <p className="text-gray-600 dark:text-gray-400">Delivery to over 200 countries worldwide</p>
          </div>
          <div className="text-center">
            <div className="bg-white dark:bg-gray-800 p-4 rounded-full w-16 h-16 mx-auto mb-4 shadow-lg">
              <Zap className="w-8 h-8 text-blue-600 mx-auto mt-2" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Fast Delivery</h3>
            <p className="text-gray-600 dark:text-gray-400">Express shipping options available</p>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default HeroSection;