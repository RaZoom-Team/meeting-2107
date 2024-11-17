import {Option} from './ui/select'


export const API_URL:string = "https://meeting2107.telegram-tools.ru/api"

const scale = 0.7
export const CROP_W = 300*scale
export const CROP_H = 552*scale

export const Literales: Option[] = [
    {key: "9n", value: "9Н"},
    {key: "9o", value: "9О"},
    {key: "9i", value: "9И"},
    {key: "9f", value: "9Ф"},
    {key: "9g", value: "9Г"},
    {key: "9v", value: "9В"},
    {key: "10k", value: "10К"},
    {key: "10c", value: "10С"},
    {key: "10p", value: "10П"},
    {key: "10u", value: "10Ю"},
    {key: "10y", value: "10У"},
    {key: "10j", value: "10Ж"},
    {key: "10z", value: "10З"},
    {key: "10i", value: "10И"},
    {key: "10t", value: "10Т"},
    {key: "10a", value: "10А"},
    {key: "10b", value: "10Б"},
    {key: "10n", value: "10Н"},
    {key: "10h", value: "10Ч"},
    {key: "10g", value: "10Ж"},
    {key: "10o", value: "10О"},
    {key: "10f", value: "10Ф"},
    {key: "11k", value: "11К"},
    {key: "11c", value: "11С"},
    {key: "11y", value: "11Ю"},
    {key: "11j", value: "11Ж"},
    {key: "11i", value: "11И"},
    {key: "11t", value: "11Т"},
    {key: "11a", value: "11А"},
    {key: "11b", value: "11Б"},
    {key: "11g", value: "11Ж"},
    {key: "11o", value: "11О"},
    {key: "11f", value: "11Ф"},
    {key: "11p", value: "11П"},
    {key: "11h", value: "11Ч"},
]

export const ErrorsText: Record<string, string> = { 
    "2000": "Вы уже зарегистрированы",
    "2001": "Аккаунт должен иметь юзернейм",
    "2002": "Слишком большой размер фотографии",
    "3000": "Вы не зарегистрированы",
    "3004": "🐝 Бз-з, вы не подписаны на Подслушано 2107",
    "3005": "Вы забанены",
}