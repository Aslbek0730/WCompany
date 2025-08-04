import React, { useState } from 'react';
import { motion } from 'framer-motion';

const Input = ({
  label,
  type = 'text',
  value,
  onChange,
  error,
  placeholder,
  required = false,
  className = '',
  ...props
}) => {
  const [focused, setFocused] = useState(false);

  return (
    <div className={`relative ${className}`}>
      {label && (
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      <motion.input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        className={`
          w-full px-4 py-3 rounded-lg border transition-all duration-200
          ${error 
            ? 'border-red-500 focus:ring-red-200' 
            : focused 
              ? 'border-blue-500 focus:ring-blue-200' 
              : 'border-gray-300 focus:ring-blue-200'
          }
          focus:outline-none focus:ring-4 bg-white dark:bg-gray-800 dark:text-white
          placeholder-gray-500 dark:placeholder-gray-400
        `}
        whileFocus={{ scale: 1.01 }}
        {...props}
      />
      {error && (
        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-2 text-sm text-red-600 dark:text-red-400"
        >
          {error}
        </motion.p>
      )}
    </div>
  );
};

export default Input;