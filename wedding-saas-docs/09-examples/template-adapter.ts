// Reference example: adapt canonical wedding data to legacy React props.
export interface WeddingData {
  schemaVersion: string;
  couple: { groom: { name: string }; bride: { name: string } };
  events: { startsAt: string; timezone: string; venue: string }[];
  gallery: string[];
}

export function toLegacyRomanticProps(data: WeddingData) {
  const event = data.events[0];
  return {
    groomName: data.couple.groom.name,
    brideName: data.couple.bride.name,
    dateLabel: event
      ? new Intl.DateTimeFormat('vi-VN', {
          dateStyle: 'long',
          timeZone: event.timezone,
        }).format(new Date(event.startsAt))
      : '',
    gallery: data.gallery,
  };
}
