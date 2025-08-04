import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Package, Search, Plus, Filter, Loader2, Eye, Edit, Trash2 } from 'lucide-react';
import Card from '../components/Card';
import { ordersAPI } from '../services/api';
import toast from 'react-hot-toast';

const OrdersPage = () => {
  const [orders, setOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setIsLoading(true);
      const response = await ordersAPI.getOrders();
      const ordersData = response.results || response;
      setOrders(ordersData);
    } catch (error) {
      console.error('Orders fetch error:', error);
      toast.error('Buyurtmalarni yuklashda xatolik yuz berdi');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteOrder = async (orderId) => {
    if (window.confirm('Bu buyurtmani o\'chirishni xohlaysizmi?')) {
      try {
        await ordersAPI.deleteOrder(orderId);
        toast.success('Buyurtma o\'chirildi');
        fetchOrders(); // Refresh the list
      } catch (error) {
        console.error('Delete order error:', error);
        toast.error('Buyurtmani o\'chirishda xatolik yuz berdi');
      }
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'processing':
        return 'text-blue-600 bg-blue-100';
      case 'in_transit':
        return 'text-yellow-600 bg-yellow-100';
      case 'delivered':
        return 'text-green-600 bg-green-100';
      case 'cancelled':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'processing':
        return 'Jarayonda';
      case 'in_transit':
        return 'Yo\'lda';
      case 'delivered':
        return 'Yetkazildi';
      case 'cancelled':
        return 'Bekor qilindi';
      default:
        return status;
    }
  };

  const filteredOrders = orders.filter(order => {
    const matchesSearch = order.order_number?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         order.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         order.destination?.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || order.status === statusFilter;
    
    return matchesSearch && matchesStatus;
  });

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      {/* Header */}
      <motion.div variants={itemVariants} className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Buyurtmalar
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Barcha buyurtmalaringizni boshqaring
          </p>
        </div>
        <button className="mt-4 sm:mt-0 inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
          <Plus className="h-4 w-4 mr-2" />
          Yangi buyurtma
        </button>
      </motion.div>

      {/* Filters */}
      <motion.div variants={itemVariants} className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Buyurtma qidirish..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div className="relative">
          <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="pl-10 pr-8 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none bg-white"
          >
            <option value="all">Barcha holatlar</option>
            <option value="processing">Jarayonda</option>
            <option value="in_transit">Yo'lda</option>
            <option value="delivered">Yetkazildi</option>
            <option value="cancelled">Bekor qilindi</option>
          </select>
        </div>
      </motion.div>

      {/* Orders List */}
      <motion.div variants={itemVariants}>
        {filteredOrders.length === 0 ? (
          <Card className="p-8 text-center">
            <Package className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              Buyurtmalar topilmadi
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              {searchTerm || statusFilter !== 'all' 
                ? 'Qidiruv natijalariga mos keladigan buyurtmalar yo\'q'
                : 'Hali buyurtmalar mavjud emas'
              }
            </p>
          </Card>
        ) : (
          <div className="grid gap-4">
            {filteredOrders.map((order, index) => (
              <motion.div
                key={order.id}
                variants={itemVariants}
                className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="flex-shrink-0">
                      <Package className="h-8 w-8 text-blue-600" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                          {order.order_number || `Buyurtma #${order.id}`}
                        </h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(order.status)}`}>
                          {getStatusText(order.status)}
                        </span>
                      </div>
                      <p className="text-gray-600 dark:text-gray-400 mt-1">
                        {order.description || order.title}
                      </p>
                      <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500 dark:text-gray-400">
                        <span>Manzil: {order.destination || order.address}</span>
                        <span>Sana: {new Date(order.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => {/* View order details */}}
                      className="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                      title="Ko'rish"
                    >
                      <Eye className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => {/* Edit order */}}
                      className="p-2 text-gray-400 hover:text-yellow-600 transition-colors"
                      title="Tahrirlash"
                    >
                      <Edit className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDeleteOrder(order.id)}
                      className="p-2 text-gray-400 hover:text-red-600 transition-colors"
                      title="O'chirish"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </motion.div>
    </motion.div>
  );
};

export default OrdersPage; 