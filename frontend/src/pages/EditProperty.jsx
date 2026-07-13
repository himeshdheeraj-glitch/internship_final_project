import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { propertyService } from '../services/api';
import { useNotifications } from '../context/NotificationContext';
import PropertyForm from '../components/Property/PropertyForm';
import Loader from '../components/Common/Loader';

const EditProperty = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { showSuccess, showError } = useNotifications();

  const [property, setProperty] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProperty = async () => {
      try {
        const data = await propertyService.getProperty(id);
        if (data) {
          setProperty(data);
        }
      } catch (err) {
        showError('Failed to load property details.');
      } finally {
        setLoading(false);
      }
    };
    fetchProperty();
  }, [id]);

  const handleFormSubmit = async (data) => {
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
        status: property?.status || 'published',
        is_featured: data.is_featured,
        amenity_ids: data.amenity_ids || [],
        purpose: data.purpose,
        parking: !!data.parking,
        furnishing_status: data.furnishing_status,
        agent_name: data.agent_name || null,
        agent_phone: data.agent_phone || null,
        agent_email: data.agent_email || null
      };

      await propertyService.updateProperty(id, payload);

      if (data.imageFile && data.imageFile.length > 0) {
        const file = data.imageFile[0];
        const img = await propertyService.uploadImage(id, file);
        if (img?.id) {
          await propertyService.setCoverImage(id, img.id);
        }
      }

      showSuccess('Property details updated!');
      navigate('/dashboard');
    } catch (err) {
      showError('Failed to update property details.');
    }
  };

  if (loading) {
    return (
      <div className="min-h-[50vh] flex items-center justify-center">
        <Loader />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-10 space-y-6">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">Edit Listing</h1>
        <p className="text-slate-500 text-sm">Update property settings, photos, and configurations.</p>
      </div>

      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 sm:p-8 rounded-3xl shadow-sm">
        <PropertyForm
          initialData={property}
          onSubmit={handleFormSubmit}
          submitLabel="Save Changes"
          onCancel={() => navigate('/dashboard')}
        />
      </div>
    </div>
  );
};

export default EditProperty;
