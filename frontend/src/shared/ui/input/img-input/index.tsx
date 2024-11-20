import createImgUrl from '../../../../widgets/crop/urlCreater'
import styles from './style.module.scss'

interface Props {
    hook: (src: string) => void
    src?: string
}

export function InputImg({hook, src}: Props) {

    const imgChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            //console.log(e.target.files[0])
            const file = e.target.files[0]
            createImgUrl(file)
            .then(hook)
            //console.log(URL.createObjectURL(e.target.files[0]))
        }
    }

    return <div style={src ? {backgroundImage: `url(${src})`} : {}} className={styles['container-input']}>
        <p style={src ? {opacity: '0'} : {}} className={styles['help']}>Нажмите, чтобы выбрать фото</p>
        <input className={styles['input']} onChange={imgChange} accept="image/jpg, image/png, image/jpeg, image/heic, image/heif, .HEIC" type='file'></input>
    </div>
}