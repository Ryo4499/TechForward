export interface User {
  userName: string | null
}

export interface Article {
  articleId: string
  title: string
  content: string
  draft: boolean
  isActivate: boolean
  createdAt: string
  updatedAt: string
  user: User
  tags: string[]
  comments: string[]
}

export interface Articles {
  result: Article[]
  count: number
}
