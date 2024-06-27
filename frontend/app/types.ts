type User = {
  id: number;
  name: string;
};

type Thread = {
  id: number;
  created_by: number;
  created_at: Date;
};

type ThreadMessage = {
  id: number;
  content: string;
  sender_id: number | null;
  thread_id: number;
  created_at: Date;
};
