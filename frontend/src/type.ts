export type Video = {
    cameraId: number,
	name: string,
	date: string,
	url: string
}

export type Camera = {
	id: number,
	name: string,
	status: string,
	type: string,
	videoIP: string,
	cameraIP: string
}
