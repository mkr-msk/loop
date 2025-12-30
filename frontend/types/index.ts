export interface Activity {
  id: number;
  name: string;
  order: number;
  is_active: boolean;
}

export interface User {
  id: number;
  tg_id: number;
}

export interface Session {
  id: number;
  activity_id: number;
  user_id: number;
  start_time: string;
  end_time: string | null;
}

export interface SessionWithActivity extends Session {
  activity: Activity;
}