export interface User {
  userId: string
  userName: string
  email: string
  createdAt: string
  updatedAt: string
  isActivate: boolean
  role: string
}

export interface UserAdmin {
  userId: string
  userName: string
  email: string
  password: string
  passwordConfirm: string
  createdAt: string
  updatedAt: string
  role: string
  isActivate: boolean
}

export interface Users {
  result: User[]
  count: number
}
