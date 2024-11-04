export type User = {
    name: string
    surname: string
    desc: string
    literal: string
    male: boolean
    is_active: boolean
    attachments: string[]
    focus_user: FocusUser
    focus_is_liked: boolean
    verify: boolean
}

export type FocusUser = Omit<User, 'is_active, focus_is_liked'>