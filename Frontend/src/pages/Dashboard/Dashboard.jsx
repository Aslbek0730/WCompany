import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Package, TrendingUp, Clock, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import Card from '../../components/Card';
import { useAuth } from '../../context/AuthContext';
import { ordersAPI, declarationsAPI } from '../../services/api';
import toast from 'react-hot-toast';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState([]);
  const [recentOrders, setRecentOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setIsLoading(true);
      
      // Fetch orders and declarations data
      const [ordersResponse, declarationsResponse] = await Promise.all([
        ordersAPI.getOrders(),
        declarationsAPI.getDeclarations()
      ]);

      // Calculate stats from real data
      const orders = ordersResponse.results || ordersResponse;
      const declarations = declarationsResponse.results || declarationsResponse;

      const newStats = [
        {
          name: 'Jami buyurtmalar',
          value: orders.length.toString(),
          change: '+2.5%',
          changeType: 'increase',
          icon: Package,
          color: 'text-blue-600'
        },
        {
          name: 'Jarayonda',
          value: orders.filter(order => order.status === 'processing').length.toString(),
          change: '-1',
          changeType: 'decrease',
          icon: Clock,
          color: 'text-yellow-600'
        },
        {
          name: 'Yetkazilgan',
          value: orders.filter(order => order.status === 'delivered').length.toString(),
          change: '+3',
          changeType: 'increase',
          icon: CheckCircle,
          color: 'text-green-600'
        },
        {
          name: 'Deklaratsiyalar',
          value: declarations.length.toString(),
          change: '0',
          changeType: 'neutral',
          icon: AlertCircle,
          color: 'text-purple-600'
        }
      ];

      // Format recent orders
      const formattedOrders = orders.slice(0, 5).map(order => ({
        id: order.order_number || order.id,
        item: order.description || order.title,
        status: order.status,
        destination: order.destination || order.address,
        date: new Date(order.created_at).toLocaleDateString(),
        statusColor: getStatusColor(order.status)
      }));

      setStats(newStats);
      setRecentOrders(formattedOrders);
    } catch (error) {
      console.error('Dashboard data fetch error:', error);
      toast.error('Ma\'lumotlarni yuklashda xatolik yuz berdi');
    } finally {
      setIsLoading(false);
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
      className="space-y-8"
    >
      {/* Welcome section */}
      <motion.div variants={itemVariants}>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Xush kelibsiz, {user?.first_name || user?.name}! 👋
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Bugungi yetkazib berishlar holati.
        </p>
      </motion.div>

      {/* Stats Grid */}
      <motion.div variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <Card key={index} className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  {stat.name}
                </p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stat.value}
                </p>
                <div className="flex items-center mt-1">
                  <span className={`text-sm font-medium ${
                    stat.changeType === 'increase' ? 'text-green-600' :
                    stat.changeType === 'decrease' ? 'text-red-600' : 'text-gray-600'
                  }`}>
                    {stat.change}
                  </span>
                  <TrendingUp className={`h-4 w-4 ml-1 ${
                    stat.changeType === 'increase' ? 'text-green-600' :
                    stat.changeType === 'decrease' ? 'text-red-600' : 'text-gray-600'
                  }`} />
                </div>
              </div>
              <div className={`p-3 rounded-full ${stat.color} bg-opacity-10`}>
                <stat.icon className="h-6 w-6" />
              </div>
            </div>
          </Card>
        ))}
      </motion.div>

      {/* Recent Orders */}
      <motion.div variants={itemVariants}>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
            So'nggi buyurtmalar
          </h2>
          <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
            Barchasini ko'rish
          </button>
        </div>
        
        <div className="space-y-4">
          {recentOrders.map((order, index) => (
            <Card key={index} className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="flex-shrink-0">
                    <Package className="h-8 w-8 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {order.item}
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {order.destination}
                    </p>
                    <p className="text-xs text-gray-400 dark:text-gray-500">
                      {order.date}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${order.statusColor}`}>
                    {order.status}
                  </span>
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {order.id}
                  </span>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </motion.div>
    </motion.div>
  );
};

export default Dashboard;