import heic2any from "heic2any"

export default async function createImgUrl(file: File) {
    if (file.name.endsWith(".heic") || file.name.endsWith(".heif")) {
        const img = await heic2any({ blob: file, toType: "image/jpeg", quality: 0.25 })
        return URL.createObjectURL(img as Blob)
    }
    return URL.createObjectURL(file)
}