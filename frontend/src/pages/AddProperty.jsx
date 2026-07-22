import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { propertyService } from '../services/api';
import { useNotifications } from '../context/NotificationContext';
import PropertyForm from '../components/Property/PropertyForm';

const AddProperty = () => {
  const navigate = useNavigate();
  const { showSuccess, showError } = useNotifications();
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFormSubmit = async (data, newFiles) => {
    try {
      const payload = {
        title: data.title,
        description: data.description,
        price: parseFloat(data.price),
        bedrooms: parseInt(data.bedrooms),
        bathrooms: parseInt(data.bathrooms),
        area: parseFloat(data.area),
        address: data.address,
        zip_code: data.zip_code,
        city_id: data.city_id,
        property_type_id: data.property_type_id,
        status: 'published',
        is_featured: data.is_featured,
        amenity_ids: data.amenity_ids || [],
        purpose: data.purpose,
        parking: !!data.parking,
        furnishing_status: data.furnishing_status,
        agent_name: data.agent_name || null,
        agent_phone: data.agent_phone || null,
        agent_email: data.agent_email || null
      };

      const newProp = await propertyService.createProperty(payload);

      // Handle Multiple Image Uploads Sequentially
      if (newFiles && newFiles.length > 0 && newProp?.id) {
        setIsUploading(true);
        setUploadProgress(0);
        
        let completed = 0;
        for (let i = 0; i < newFiles.length; i++) {
          const file = newFiles[i];
          await propertyService.uploadImage(newProp.id, file, (percent) => {
            const currentContribution = percent / newFiles.length;
            const overallPercent = Math.round(((completed / newFiles.length) * 100) + currentContribution);
            setUploadProgress(overallPercent);
          });
          completed++;
          setUploadProgress(Math.round((completed / newFiles.length) * 100));
        }
      }

      showSuccess('Property published successfully!');
      navigate('/dashboard');
    } catch (err) {
      const backendMessage = err?.response?.data?.message;
      showError(backendMessage || 'Failed to publish property.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-10 space-y-6">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">List New Property</h1>
        <p className="text-slate-500 text-sm">Add a new verified listing to the catalog.</p>
      </div>

      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 sm:p-8 rounded-3xl shadow-sm">
        <PropertyForm
          onSubmit={handleFormSubmit}
          submitLabel="Publish Property"
          onCancel={() => navigate('/dashboard')}
          uploadProgress={uploadProgress}
          isUploading={isUploading}
        />
      </div>
    </div>
  );
};

export default AddProperty;
