export const normalizeUser = (userData) => {
  if (!userData) return null;

  const roleName =
    typeof userData.role === 'string'
      ? userData.role
      : userData.role?.name || userData.role_name || 'buyer';

  return {
    ...userData,
    role: roleName,
    role_name: roleName,
  };
};
