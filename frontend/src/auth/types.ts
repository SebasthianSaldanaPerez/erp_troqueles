export type UserRole =
  | "ADMIN"
  | "OPERATOR"
  | "VIEWER";

export type CurrentUser = {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  status: string;
};