import React from 'react';
import { motion } from 'framer-motion';
import HeroSection from './HeroSection';
import ServicesSection from './ServicesSection';
import Testimonials from './Testimonials';
import ContactSection from './ContactSection';

const LandingPage = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <HeroSection />
      <ServicesSection />
      <Testimonials />
      <ContactSection />
    </motion.div>
  );
};

export default LandingPage;