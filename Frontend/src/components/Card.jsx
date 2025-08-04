import React from 'react';
import { motion } from 'framer-motion';

const Card = ({ 
  children, 
  className = '', 
  hover = true, 
  onClick,
  ...props 
}) => {
  return (
    <motion.div
      className={`
        bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700
        ${hover ? 'hover:shadow-xl cursor-pointer' : ''} 
        ${className}
      `}
      whileHover={hover ? { y: -4, scale: 1.02 } : {}}
      whileTap={onClick ? { scale: 0.98 } : {}}
      onClick={onClick}
      {...props}
    >
      {children}
    </motion.div>
  );
};

export default Card;