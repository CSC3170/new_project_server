interface IUser {
  user_id: number;
  name: string;
  is_admin: boolean;
  nickname: string | null;
  email: string | null;
  phone: string | null;
}

export { type IUser };
