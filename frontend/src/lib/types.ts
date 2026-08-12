export type UserRole = "CUSTOMER" | "SALE" | "COORDINATOR" | "ADMIN";

export interface User {
  id: string;
  full_name: string;
  email: string;
  phone: string | null;
  role: UserRole;
  status: "ACTIVE" | "LOCKED" | "DISABLED";
}

export interface PropertyMedia {
  id?: string;
  url: string;
  is_cover?: boolean;
  caption?: string | null;
}

export interface Property {
  id: string;
  code: string;
  property_kind: string;
  title: string;
  description?: string | null;
  status: string;
  address_line?: string | null;
  address_full?: string | null;
  ward?: string | null;
  district?: string | null;
  province?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  area_sqm: number;
  bedrooms?: number | null;
  bathrooms?: number | null;
  list_price?: number | null;
  currency: string;
  features?: Record<string, unknown>;
  media: PropertyMedia[];
  image?: string | null;
}

export interface SaleSummary {
  id: string;
  full_name: string;
  phone: string | null;
  email: string;
  job_title?: string | null;
}

export interface Booking {
  id: string;
  request_code: string;
  status: string;
  preferred_start: string;
  preferred_end: string;
  party_size: number;
  customer_note?: string | null;
  created_at: string;
  expires_at?: string | null;
  property: {
    id: string;
    title: string;
    address: string;
    district?: string | null;
    province?: string | null;
    media: PropertyMedia[];
  };
  sale?: SaleSummary | null;
  customer?: Pick<User, "id" | "full_name" | "phone" | "email">;
  appointment?: {
    id: string;
    booking_code: string;
    status: string;
    starts_at: string;
    ends_at: string;
  } | null;
}

export interface AvailabilitySlot {
  sale_user_id: string;
  sale_name: string;
  starts_at: string;
  ends_at: string;
  label: string;
}
