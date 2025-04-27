import { getToken } from './auth';

export const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function fetchMenu() {
  const response = await fetch(`${API_URL}/menu`);
  if (!response.ok) {
    throw new Error('Failed to fetch menu');
  }
  return response.json();
}

export async function createOrder(orderData: any) {
  const token = getToken();
  const response = await fetch(`${API_URL}/orders`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`, // Agregar el token JWT
    },
    body: JSON.stringify(orderData),
  });
  if (!response.ok) {
    throw new Error('Failed to create order');
  }
  return response.json();
}

export async function loginUser(email: string, password: string) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) {
    throw new Error('Failed to log in');
  }
  return response.json(); // Devuelve el token JWT
}

export async function registerUser(userData: any) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });
  if (!response.ok) {
    throw new Error('Failed to register user');
  }
  return response.json();
}

export async function updateUserProfile(userId: number, updatedData: any) {
  const response = await fetch(`${API_URL}/auth/update-profile`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId, ...updatedData }),
  });
  if (!response.ok) {
    throw new Error('Failed to update user profile');
  }
  return response.json();
}

export async function changePassword(userId: number, currentPassword: string, newPassword: string) {
  const response = await fetch(`${API_URL}/auth/change-password`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId, current_password: currentPassword, new_password: newPassword }),
  });
  if (!response.ok) {
    throw new Error('Failed to change password');
  }
  return response.json();
}

export async function forgotPassword(email: string) {
  const response = await fetch(`${API_URL}/auth/forgot-password`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email }),
  });
  if (!response.ok) {
    throw new Error('Failed to send password reset email');
  }
  return response.json();
}

export async function resetPassword(token: string, newPassword: string) {
  const response = await fetch(`${API_URL}/auth/reset-password`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ token, new_password: newPassword }),
  });
  if (!response.ok) {
    throw new Error('Failed to reset password');
  }
  return response.json();
}

export async function saveCart(userId: number, cartItems: any[]) {
  const response = await fetch(`${API_URL}/cart`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId, cart_items: cartItems }),
  });
  if (!response.ok) {
    throw new Error('Failed to save cart');
  }
  return response.json();
}

export async function getCart(userId: number) {
  const response = await fetch(`${API_URL}/cart?user_id=${userId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch cart');
  }
  return response.json();
}

export async function sendNotification(userId: number, message: string, type: string = 'info') {
  const response = await fetch(`${API_URL}/notifications`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId, message, type }),
  });
  if (!response.ok) {
    throw new Error('Failed to send notification');
  }
  return response.json();
}

export async function getNotifications(userId: number) {
  const response = await fetch(`${API_URL}/notifications?user_id=${userId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch notifications');
  }
  return response.json();
}

export async function addAddress(userId: number, addressData: any) {
  const response = await fetch(`${API_URL}/addresses`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId, address: addressData }),
  });
  if (!response.ok) {
    throw new Error('Failed to add address');
  }
  return response.json();
}

export async function listAddresses(userId: number) {
  const response = await fetch(`${API_URL}/addresses?user_id=${userId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch addresses');
  }
  return response.json();
}

export async function deleteAddress(addressId: number) {
  const response = await fetch(`${API_URL}/addresses/${addressId}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error('Failed to delete address');
  }
  return response.json();
}

export async function getPaymentHistory(userId: number) {
  const response = await fetch(`${API_URL}/payments/history?user_id=${userId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch payment history');
  }
  return response.json();
}

export async function sendSupportMessage(userId: number, subject: string, message: string) {
  const response = await fetch(`${API_URL}/support/messages`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId, subject, message }),
  });
  if (!response.ok) {
    throw new Error('Failed to send support message');
  }
  return response.json();
}

export async function getSupportMessages(userId: number) {
  const response = await fetch(`${API_URL}/support/messages?user_id=${userId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch support messages');
  }
  return response.json();
}

export async function getDeliveryStatus(orderId: number) {
  const response = await fetch(`${API_URL}/delivery/status?order_id=${orderId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch delivery status');
  }
  return response.json();
}

export async function getUserStats(userId: number) {
  const response = await fetch(`${API_URL}/stats/user?user_id=${userId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch user stats');
  }
  return response.json();
}

export async function updateStock(itemId: number, quantity: number) {
  const response = await fetch(`${API_URL}/inventory/update`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ item_id: itemId, quantity }),
  });
  if (!response.ok) {
    throw new Error('Failed to update stock');
  }
  return response.json();
}

export async function checkAvailability(items: { item_id: number; quantity: number }[]) {
  const response = await fetch(`${API_URL}/inventory/check`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ items }),
  });
  if (!response.ok) {
    throw new Error('Failed to check availability');
  }
  return response.json();
}
