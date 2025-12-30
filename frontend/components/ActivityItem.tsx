'use client';

import { Activity } from '@/types';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

interface ActivityItemProps {
  activity: Activity;
  onDelete: (id: number) => void;
  onToggleActive: (id: number, is_active: boolean) => void;
}

export default function ActivityItem({ activity, onDelete, onToggleActive }: ActivityItemProps) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id: activity.id,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`bg-slate-500 rounded-lg shadow p-4 flex items-center gap-4 ${
        !activity.is_active ? 'opacity-50' : ''
      }`}
    >
      <div
        {...attributes}
        {...listeners}
        className="cursor-grab active:cursor-grabbing text-gray-400 hover:text-gray-600"
      >
        <svg
          className="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 8h16M4 16h16"
          />
        </svg>
      </div>

      <div className="flex-1 ">
        <h3 className="font-bold text-2xl">{activity.name}</h3>
      </div>

      <button
        onClick={() => onToggleActive(activity.id, !activity.is_active)}
        className={`px-3 py-1 rounded text-sm ${
          activity.is_active
            ? 'bg-slate-500 text-green-400'
            : 'bg-slate-500 text-gray-700'
        }`}
      >
        {activity.is_active ? 'Активна' : 'Неактивна'}
      </button>

      <button
        onClick={() => onDelete(activity.id)}
        className="px-3 py-1 bg-red-100 text-red-700 rounded text-sm hover:bg-red-200 transition"
      >
        Удалить
      </button>
    </div>
  );
}