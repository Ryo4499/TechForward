export interface User {
  userName: string
}

export interface ArticleAdmin {
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

export interface ArticlesAdmin {
  result: ArticleAdmin[]
  count: number
}
