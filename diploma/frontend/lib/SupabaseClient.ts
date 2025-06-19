import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://yndbynxapukqmtykwplw.supabase.co'
const supabaseAnonKey = '<eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluZGJ5bnhhcHVrcW10eWt3cGx3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTQyMTgxNCwiZXhwIjoyMDYwOTk3ODE0fQ.n4ohc1dLfsYtyXb8PvGYrwsfH5JHGFa3DAzJqxSdeyI>'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
