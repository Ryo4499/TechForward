export interface User {
  userName: string
}

export interface Comment {
  commentId: string
  content: string
  createdAt: string
  updatedAt: string
  article: string
  user: User
  edit: boolean
  editText: string
}

export interface Comments {
  result: Comment[]
  count: number
}
