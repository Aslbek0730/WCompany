import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import { User, Mail, Lock, Eye, EyeOff, Phone, Truck } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import Button from '../../components/Button';
import Input from '../../components/Input';
import toast from 'react-hot-toast';

const Register = () => {
  const [formData, setFormData] = useState({
    name: '',
    surname: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const { register } = useAuth();
  const navigate = useNavigate();

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'First name is required';
    }
    
    if (!formData.surname.trim()) {
      newErrors.surname = 'Last name is required';
    }
    
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }
    
    if (!formData.phone) {
      newErrors.phone = 'Phone number is required';
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    setLoading(true);
    try {
      await register(formData);
      toast.success('Account created successfully!');
      navigate('/dashboard');
    } catch (error) {
      toast.error('Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl w-full">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 bg-white dark:bg-gray-800 rounded-2xl shadow-2xl overflow-hidden">
          {/* Left side - Animation */}
          <div className="hidden lg:flex items-center justify-center bg-gradient-to-br from-purple-600 to-pink-700 relative overflow-hidden">
            <div className="absolute inset-0">
              <motion.div
                className="absolute top-1/3 left-1/3 w-40 h-40 bg-white rounded-full opacity-10"
                animate={{
                  y: [0, -50, 0],
                  x: [0, 30, 0],
                }}
                transition={{
                  duration: 18,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />
              <motion.div
                className="absolute bottom-1/3 right-1/3 w-28 h-28 bg-white rounded-full opacity-10"
                animate={{
                  y: [0, 40, 0],
                  x: [0, -20, 0],
                }}
                transition={{
                  duration: 22,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />
            </div>
            <div className="relative z-10 text-center text-white">
              <motion.div
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ duration: 0.8 }}
                className="bg-white bg-opacity-20 p-6 rounded-full mb-6 mx-auto w-24 h-24 flex items-center justify-center"
              >
                <Truck size={48} />
              </motion.div>
              <motion.h2
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="text-3xl font-bold mb-4"
              >
                Join WorldCompany
              </motion.h2>
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.4 }}
                className="text-lg opacity-90"
              >
                Start shipping globally today
              </motion.p>
            </div>
          </div>

          {/* Right side - Form */}
          <div className="p-8 lg:p-12">
            <div className="text-center mb-8">
              <div className="flex items-center justify-center lg:hidden mb-6">
                <div className="bg-blue-600 p-3 rounded-lg">
                  <Truck className="h-8 w-8 text-white" />
                </div>
                <span className="text-2xl font-bold text-gray-900 dark:text-white ml-3">
                  WorldCompany
                </span>
              </div>
              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="text-3xl font-bold text-gray-900 dark:text-white mb-2"
              >
                Create Account
              </motion.h1>
              <p className="text-gray-600 dark:text-gray-400">
                Join thousands of customers worldwide
              </p>
            </div>

            <motion.form
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              onSubmit={handleSubmit}
              className="space-y-6"
            >
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="relative">
                  <User className="absolute left-3 top-12 h-5 w-5 text-gray-400" />
                  <Input
                    label="First Name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    error={errors.name}
                    placeholder="Enter your first name"
                    className="pl-10"
                    required
                  />
                </div>
                <div className="relative">
                  <User className="absolute left-3 top-12 h-5 w-5 text-gray-400" />
                  <Input
                    label="Last Name"
                    name="surname"
                    value={formData.surname}
                    onChange={handleChange}
                    error={errors.surname}
                    placeholder="Enter your last name"
                    className="pl-10"
                    required
                  />
                </div>
              </div>

              <div className="relative">
                <Mail className="absolute left-3 top-12 h-5 w-5 text-gray-400" />
                <Input
                  label="Email Address"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  error={errors.email}
                  placeholder="Enter your email"
                  className="pl-10"
                  required
                />
              </div>

              <div className="relative">
                <Phone className="absolute left-3 top-12 h-5 w-5 text-gray-400" />
                <Input
                  label="Phone Number"
                  name="phone"
                  type="tel"
                  value={formData.phone}
                  onChange={handleChange}
                  error={errors.phone}
                  placeholder="Enter your phone number"
                  className="pl-10"
                  required
                />
              </div>

              <div className="relative">
                <Lock className="absolute left-3 top-12 h-5 w-5 text-gray-400" />
                <Input
                  label="Password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  value={formData.password}
                  onChange={handleChange}
                  error={errors.password}
                  placeholder="Create a password"
                  className="pl-10 pr-10"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-12 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>

              <div className="relative">
                <Lock className="absolute left-3 top-12 h-5 w-5 text-gray-400" />
                <Input
                  label="Confirm Password"
                  name="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  error={errors.confirmPassword}
                  placeholder="Confirm your password"
                  className="pl-10 pr-10"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3 top-12 text-gray-400 hover:text-gray-600"
                >
                  {showConfirmPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  required
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="ml-2 text-sm text-gray-600 dark:text-gray-400">
                  I agree to the{' '}
                  <Link to="/terms" className="text-blue-600 hover:text-blue-500">
                    Terms of Service
                  </Link>{' '}
                  and{' '}
                  <Link to="/privacy" className="text-blue-600 hover:text-blue-500">
                    Privacy Policy
                  </Link>
                </span>
              </div>

              <Button
                type="submit"
                size="lg"
                loading={loading}
                className="w-full"
              >
                Create Account
              </Button>

              <div className="text-center">
                <span className="text-gray-600 dark:text-gray-400">
                  Already have an account?{' '}
                </span>
                <Link
                  to="/login"
                  className="text-blue-600 hover:text-blue-500 font-medium"
                >
                  Sign in
                </Link>
              </div>
            </motion.form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;