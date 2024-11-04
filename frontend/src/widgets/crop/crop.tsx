import { ReactElement, useState } from "react";
import Cropper, { Area, Point } from "react-easy-crop";
import { Button, CROP_H, CROP_W } from "../../shared";
import getCroppedImg from "./toImg";
import styles from './style.module.scss'

interface Props {
    img: string
    setImg: (img: string | undefined) => void
    onComplete: () => void
}

export function CropWidget({img, setImg, onComplete}: Props): ReactElement {
    const [zoom, setZoom] = useState(1.2)
    const [crop, setCrop] = useState<Point>({x: 0, y: 0})
    const [area, setArea] = useState<Area | null>(null)

    const completeCrop = () => {
        if (area) {
            getCroppedImg(img, area).then((newImg) => {
                if (newImg) {
                    setImg(newImg);
                }
            })
        }
        onComplete();
    }

    const deleteCrop = () => {
        setImg(undefined)
        onComplete();
    }

    const onCropComplete = (_croppedArea: Area, croppedAreaPixels: Area) => {
        setArea(croppedAreaPixels)
    }

    const style = {
        border: '2px dashed',
        borderColor: 'var(--main-color)',
        borderRadius: '8px'
    }

    const cropper = <Cropper
        style={{cropAreaStyle: style}}
        image={img}
        showGrid={false}
        cropSize={{width: CROP_W, height: CROP_H}}
        zoom={zoom}
        crop={crop}
        onZoomChange={setZoom}
        onCropChange={setCrop}
        onCropComplete={onCropComplete}
    />

    return <div className={styles['main']}>
        <div style={{position: "relative"}} className={styles['container-cropper']}>
            {cropper}
        </div>
        <div className={styles['buttons']}>
            <Button active={true} text="Сохранить" hook={completeCrop}/>
            <Button style="outfill" active={true} text="Отменить" hook={deleteCrop}/>
        </div>
    </div>
}