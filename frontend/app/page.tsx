'use client';

import { useEffect, useState } from 'react';
import { Activity } from '@/types';
import { activityApi } from '@/lib/api';
import ActivityList from '@/components/ActivityList';
import ActivityForm from '@/components/ActivityForm';

export default function Home() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadActivities();
  }, []);

  const loadActivities = async () => {
    try {
      const response = await activityApi.getAll();
      setActivities(response.data);
    } catch (error) {
      console.error('Failed to load activities:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReorder = async (newOrder: Activity[]) => {
    setActivities(newOrder);
    try {
      const activity_ids = newOrder.map(a => a.id);
      await activityApi.reorder(activity_ids);
    } catch (error) {
      console.error('Failed to reorder:', error);
      loadActivities(); // Reload on error
    }
  };

  const handleCreate = async (name: string) => {
    try {
      await activityApi.create({
        name,
        order: activities.length,
        is_active: true,
      });
      loadActivities();
    } catch (error) {
      console.error('Failed to create:', error);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await activityApi.delete(id);
      loadActivities();
    } catch (error) {
      console.error('Failed to delete:', error);
    }
  };

  const handleToggleActive = async (id: number, is_active: boolean) => {
    try {
      await activityApi.update(id, { is_active });
      loadActivities();
    } catch (error) {
      console.error('Failed to update:', error);
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  return (
    <main className="min-h-screen p-8 bg-slate-900">
      <div className="max-w-2xl mx-auto flex flex-col">
        <h1 className="text-4xl font-bold mb-8 w-full text-center">Loop L1</h1>
        
        <ActivityForm onSubmit={handleCreate} />

        <ActivityList
          activities={activities}
          onReorder={handleReorder}
          onDelete={handleDelete}
          onToggleActive={handleToggleActive}
        />
      </div>
    </main>
  );
}