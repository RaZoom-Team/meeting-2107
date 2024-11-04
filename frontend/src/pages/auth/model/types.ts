export enum Stage {
    SUBINFO = 0,
    NAME = 1,
    PHOTO = 2,
    ABOUT = 3
}

export enum Sex {
    MALE = "Мужчина",
    WOMAN = "Женщина",
}

export interface UserRegister {
    name: string
    surname: string
    literal: string
    male: boolean
    desc: string
}
