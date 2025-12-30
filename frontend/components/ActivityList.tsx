'use client';

import { Activity } from '@/types';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import ActivityItem from './ActivityItem';

interface ActivityListProps {
  activities: Activity[];
  onReorder: (activities: Activity[]) => void;
  onDelete: (id: number) => void;
  onToggleActive: (id: number, is_active: boolean) => void;
}

export default function ActivityList({
  activities,
  onReorder,
  onDelete,
  onToggleActive,
}: ActivityListProps) {
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      const oldIndex = activities.findIndex((item) => item.id === active.id);
      const newIndex = activities.findIndex((item) => item.id === over.id);

      const newOrder = arrayMove(activities, oldIndex, newIndex).map((item, index) => ({
        ...item,
        order: index,
      }));

      onReorder(newOrder);
    }
  };

  if (activities.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        Нет активностей. Добавьте первую активность выше.
      </div>
    );
  }

  return (
    <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
      <SortableContext items={activities.map((a) => a.id)} strategy={verticalListSortingStrategy}>
        <div className="space-y-2">
          {activities.map((activity) => (
            <ActivityItem
              key={activity.id}
              activity={activity}
              onDelete={onDelete}
              onToggleActive={onToggleActive}
            />
          ))}
        </div>
      </SortableContext>
    </DndContext>
  );
}