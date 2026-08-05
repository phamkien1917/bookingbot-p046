BEGIN;

INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('0cd29177-3f37-40b8-b63c-2ff44de00f79', 'SALE', 'sale_24441997@example.com', '(391)444-7677', 'HASH', 'timphong', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('0cd29177-3f37-40b8-b63c-2ff44de00f79', 'EMP-A_24441997', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('595adcab-6060-4a0a-81c1-eb238a20dabf', 'SALE', 'sale_31290308@example.com', '001-429-600-5337x2483', 'HASH', 'Trần Quân', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('595adcab-6060-4a0a-81c1-eb238a20dabf', 'EMP-A_31290308', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('e22b8d72-49d3-4a82-9c81-c83cb2a7d905', 'SALE', 'sale_25505101@example.com', '813-790-6615x702', 'HASH', 'Gia Ân', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('e22b8d72-49d3-4a82-9c81-c83cb2a7d905', 'EMP-A_25505101', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('973f4d6e-bc58-467e-86ce-8b515702fd93', 'SALE', 'sale_8693691@example.com', '3034679842', 'HASH', 'Tài', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('973f4d6e-bc58-467e-86ce-8b515702fd93', 'EMP-A_8693691', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('679c3af4-0ff3-4be9-9cd6-f0aacd721010', 'SALE', 'sale_32260246@example.com', '473.785.7758x8533', 'HASH', 'Ngọc Long', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('679c3af4-0ff3-4be9-9cd6-f0aacd721010', 'EMP-A_32260246', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('93cf20fd-efc6-4b60-b286-8324f310474c', 'SALE', 'sale_26299185@example.com', '891.699.9961', 'HASH', 'Nguyễn Phước Neway Home ', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('93cf20fd-efc6-4b60-b286-8324f310474c', 'EMP-A_26299185', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('25db544d-b636-482c-95ce-102c3c6864d1', 'SALE', 'sale_12517435@example.com', '+1-599-825-8848x04067', 'HASH', 'Hữu Thắng Apartment', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('25db544d-b636-482c-95ce-102c3c6864d1', 'EMP-A_12517435', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('9322c63a-1dce-4fe4-9106-7102336991d1', 'SALE', 'sale_22186234@example.com', '882-251-7388x2339', 'HASH', 'hà pihomes', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('9322c63a-1dce-4fe4-9106-7102336991d1', 'EMP-A_22186234', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('4f95a3fe-8dc5-410c-a131-0782dfa7e95c', 'SALE', 'sale_16240454@example.com', '679.537.9297x7266', 'HASH', 'Nguyễn Vũ Khôi', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('4f95a3fe-8dc5-410c-a131-0782dfa7e95c', 'EMP-A_16240454', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('fa0d26b8-a093-46ac-b083-ed794259ebe4', 'SALE', 'sale_30707629@example.com', '4653498917', 'HASH', 'An an an', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('fa0d26b8-a093-46ac-b083-ed794259ebe4', 'EMP-A_30707629', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('a83c97ee-e832-4e44-93aa-ef4031eb6358', 'SALE', 'sale_30233886@example.com', '001-636-807-1651x49504', 'HASH', 'Nhật Thiên Airways Unitegroup', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('a83c97ee-e832-4e44-93aa-ef4031eb6358', 'EMP-A_30233886', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('c7edf03e-5da2-42c3-ad48-53160a37b598', 'SALE', 'sale_17359097@example.com', '+1-742-736-7995x21417', 'HASH', 'nguyen anh', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('c7edf03e-5da2-42c3-ad48-53160a37b598', 'EMP-A_17359097', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('45988484-9573-493b-98f4-6e9e7e631e6e', 'SALE', 'sale_15824422@example.com', '(950)855-3577x8736', 'HASH', 'Nhung', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('45988484-9573-493b-98f4-6e9e7e631e6e', 'EMP-A_15824422', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('6c3d3653-e6bb-4301-b612-2517c2744784', 'SALE', 'sale_22184253@example.com', '6813161003', 'HASH', 'Hà Dương Apartment', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('6c3d3653-e6bb-4301-b612-2517c2744784', 'EMP-A_22184253', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('35cf7e2c-253f-48c7-a54f-2aecab70aa82', 'SALE', 'sale_29248849@example.com', '001-273-593-5599', 'HASH', 'Kun cho thuê ', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('35cf7e2c-253f-48c7-a54f-2aecab70aa82', 'EMP-A_29248849', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('1f8ce52e-d86a-4449-9b17-9a3099edd273', 'SALE', 'sale_17194237@example.com', '+1-471-595-8625', 'HASH', 'Huyền Nguyễn', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('1f8ce52e-d86a-4449-9b17-9a3099edd273', 'EMP-A_17194237', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('0272920e-e1ad-46ec-82f0-195ce35a620c', 'SALE', 'sale_27739572@example.com', '(569)885-6507x80180', 'HASH', 'Lê Kỳ', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('0272920e-e1ad-46ec-82f0-195ce35a620c', 'EMP-A_27739572', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('19759e56-f845-4ce3-b05b-04971fc2d91d', 'SALE', 'sale_27624940@example.com', '870.312.2592x0004', 'HASH', 'Liên', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('19759e56-f845-4ce3-b05b-04971fc2d91d', 'EMP-A_27624940', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('215b1693-a2f3-4bba-a019-5742093e3387', 'SALE', 'sale_26347869@example.com', '(463)839-4527x14073', 'HASH', 'Mỹ Tâm', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('215b1693-a2f3-4bba-a019-5742093e3387', 'EMP-A_26347869', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('f1d72b2b-7977-42e0-ac4d-06f9bda20f2d', 'SALE', 'sale_22292188@example.com', '(991)376-5969x4462', 'HASH', 'Nguyễn Trung Trực', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('f1d72b2b-7977-42e0-ac4d-06f9bda20f2d', 'EMP-A_22292188', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('6e71b008-9825-4628-9790-375875048ca1', 'SALE', 'sale_25281832@example.com', '(959)477-6672', 'HASH', 'Võ Thái Tuấn HiFriendz', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('6e71b008-9825-4628-9790-375875048ca1', 'EMP-A_25281832', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('d4442132-86b7-40cc-8522-37f248b64f0b', 'SALE', 'sale_24148153@example.com', '602.959.4173x9668', 'HASH', 'Thanh Hương', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('d4442132-86b7-40cc-8522-37f248b64f0b', 'EMP-A_24148153', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('58064905-50a6-489c-a056-6fc61d73b0ff', 'SALE', 'sale_12638993@example.com', '(426)731-4320x8176', 'HASH', 'LIGHTHOUSE', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('58064905-50a6-489c-a056-6fc61d73b0ff', 'EMP-A_12638993', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('ff169240-13ee-4788-8624-768d78db78fc', 'SALE', 'sale_1309573@example.com', '5047680964', 'HASH', 'Thảo lượm', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('ff169240-13ee-4788-8624-768d78db78fc', 'EMP-A_1309573', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('83c30720-7756-4038-9086-e6c69336cfe8', 'SALE', 'sale_24074944@example.com', '461.515.0911', 'HASH', 'Nguyễn Phúc Vinh', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('83c30720-7756-4038-9086-e6c69336cfe8', 'EMP-A_24074944', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('956c3b8b-2e9e-4e40-aa11-c88a74e4f2ac', 'SALE', 'sale_10190568@example.com', '001-338-851-7212x4909', 'HASH', 'Minh Khoa apartment ', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('956c3b8b-2e9e-4e40-aa11-c88a74e4f2ac', 'EMP-A_10190568', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('1923b3f3-5600-4e41-a297-2ab6948698f5', 'SALE', 'sale_26632219@example.com', '001-441-750-8383x089', 'HASH', 'Thái Thịnh HiFriendz', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('1923b3f3-5600-4e41-a297-2ab6948698f5', 'EMP-A_26632219', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('3d23ad21-d92e-4f40-a753-6e506eeccbb1', 'SALE', 'sale_2137548@example.com', '(518)462-8278x16458', 'HASH', 'TyTy phòng thuê chính chủ ', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('3d23ad21-d92e-4f40-a753-6e506eeccbb1', 'EMP-A_2137548', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('e7249ca8-47a8-4952-8f33-1a5bb456d7e4', 'SALE', 'sale_5088224@example.com', '(560)848-4635x6267', 'HASH', 'Lê Hoa', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('e7249ca8-47a8-4952-8f33-1a5bb456d7e4', 'EMP-A_5088224', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('54e9eecf-6b06-49cf-80d8-97324ff1a013', 'SALE', 'sale_9889628@example.com', '452-694-9310x092', 'HASH', 'Phòng Kinh Doanh', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO sale_profiles (user_id, employee_code, max_daily_tours, calendar_provider)
VALUES ('54e9eecf-6b06-49cf-80d8-97324ff1a013', 'EMP-A_9889628', 8, 'GOOGLE') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('951118ab-8658-4ec2-86b8-09aa4afd07e6', 'CUSTOMER', 'customer0@example.com', '+1-675-743-9435', 'HASH', 'Jill Foster', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('951118ab-8658-4ec2-86b8-09aa4afd07e6', 'CUS-C001') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('b3133afe-fbd0-4ce4-94f2-94c77ff3b96d', 'CUSTOMER', 'customer1@example.com', '9354333889', 'HASH', 'Katelyn Hill', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('b3133afe-fbd0-4ce4-94f2-94c77ff3b96d', 'CUS-C002') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('0c6b41b9-d6a8-4268-b954-3bab904a9e1f', 'CUSTOMER', 'customer2@example.com', '(729)343-1918', 'HASH', 'Juan Carroll', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('0c6b41b9-d6a8-4268-b954-3bab904a9e1f', 'CUS-C003') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('facacdec-cad7-4145-b0b7-edeb691bbc86', 'CUSTOMER', 'customer3@example.com', '9233801719', 'HASH', 'Jesus Harrison', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('facacdec-cad7-4145-b0b7-edeb691bbc86', 'CUS-C004') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('c06efeb1-349e-445c-a8bb-56a8cb7c0499', 'CUSTOMER', 'customer4@example.com', '001-864-714-6177x12087', 'HASH', 'Barbara Santiago', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('c06efeb1-349e-445c-a8bb-56a8cb7c0499', 'CUS-C005') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('2d8bcc17-6257-42a5-bd35-7e167363acb6', 'CUSTOMER', 'customer5@example.com', '001-416-568-8572', 'HASH', 'Colin Nunez', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('2d8bcc17-6257-42a5-bd35-7e167363acb6', 'CUS-C006') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('84e68e2b-0b42-4cdd-9023-823e0fab9fbe', 'CUSTOMER', 'customer6@example.com', '+1-293-766-0707', 'HASH', 'Megan Wright', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('84e68e2b-0b42-4cdd-9023-823e0fab9fbe', 'CUS-C007') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('a5384434-4d00-44a0-b31f-a1e590ad287c', 'CUSTOMER', 'customer7@example.com', '+1-631-472-3871x542', 'HASH', 'Patricia Cobb', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('a5384434-4d00-44a0-b31f-a1e590ad287c', 'CUS-C008') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('25004382-bc56-457d-bbc5-71f9bbb2e032', 'CUSTOMER', 'customer8@example.com', '001-923-664-3069x91571', 'HASH', 'Michael Barnett', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('25004382-bc56-457d-bbc5-71f9bbb2e032', 'CUS-C009') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('2e492d28-ca6e-4811-af15-d9bf08ef8c1e', 'CUSTOMER', 'customer9@example.com', '+1-557-273-2337', 'HASH', 'Jennifer Henderson', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('2e492d28-ca6e-4811-af15-d9bf08ef8c1e', 'CUS-C010') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('ca445c6d-04c3-4ce2-9491-762faf919202', 'CUSTOMER', 'customer10@example.com', '(482)532-9303', 'HASH', 'Joseph Miller', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('ca445c6d-04c3-4ce2-9491-762faf919202', 'CUS-C011') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('5557664e-95a7-49a4-bb2f-339c7b5e2302', 'CUSTOMER', 'customer11@example.com', '5813131407', 'HASH', 'Alexander Conway', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('5557664e-95a7-49a4-bb2f-339c7b5e2302', 'CUS-C012') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('5c119de8-c731-4506-92af-d61bd921af0e', 'CUSTOMER', 'customer12@example.com', '001-803-905-6917x07117', 'HASH', 'Lawrence Long', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('5c119de8-c731-4506-92af-d61bd921af0e', 'CUS-C013') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('c7aa753f-0e33-4c92-ac86-4a904815c30e', 'CUSTOMER', 'customer13@example.com', '+1-930-410-4901', 'HASH', 'Stephanie Anderson', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('c7aa753f-0e33-4c92-ac86-4a904815c30e', 'CUS-C014') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('4fb71bc9-7dac-4a6a-8f33-7b61015c46af', 'CUSTOMER', 'customer14@example.com', '(868)452-1650x7388', 'HASH', 'Richard Quinn', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('4fb71bc9-7dac-4a6a-8f33-7b61015c46af', 'CUS-C015') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('3e7c589e-ee59-4d5f-8429-bb37f5fc2f04', 'CUSTOMER', 'customer15@example.com', '700-949-8615x591', 'HASH', 'Ethan Davis', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('3e7c589e-ee59-4d5f-8429-bb37f5fc2f04', 'CUS-C016') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('59a7951d-57fc-46b7-9358-e73976a4d9fb', 'CUSTOMER', 'customer16@example.com', '+1-282-776-7892x445', 'HASH', 'Michael Payne', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('59a7951d-57fc-46b7-9358-e73976a4d9fb', 'CUS-C017') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('bd114457-dcb2-4306-8dbe-b3165fea2aea', 'CUSTOMER', 'customer17@example.com', '3829740948', 'HASH', 'Adam Daniels', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('bd114457-dcb2-4306-8dbe-b3165fea2aea', 'CUS-C018') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('424c5576-3002-4b9b-a8cf-e28af4a5f938', 'CUSTOMER', 'customer18@example.com', '336.472.3389', 'HASH', 'Jeffrey Johnson', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('424c5576-3002-4b9b-a8cf-e28af4a5f938', 'CUS-C019') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('e9d6c3d5-6a00-4802-a5f3-560b737b5e4c', 'CUSTOMER', 'customer19@example.com', '(494)454-0209x87935', 'HASH', 'Kara Hurley', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('e9d6c3d5-6a00-4802-a5f3-560b737b5e4c', 'CUS-C020') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('c9edde11-2674-4b68-b465-b4287991e658', 'CUSTOMER', 'customer20@example.com', '001-826-679-0169', 'HASH', 'Leslie Hall', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('c9edde11-2674-4b68-b465-b4287991e658', 'CUS-C021') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('74d41871-74fd-4bab-a942-43869a233df9', 'CUSTOMER', 'customer21@example.com', '+1-960-595-1737x9821', 'HASH', 'Brandon Stokes', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('74d41871-74fd-4bab-a942-43869a233df9', 'CUS-C022') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('161dd102-c172-4888-9e98-b8a892ab4fd1', 'CUSTOMER', 'customer22@example.com', '001-982-353-9717x55767', 'HASH', 'Sandra Thomas', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('161dd102-c172-4888-9e98-b8a892ab4fd1', 'CUS-C023') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('730d3924-159d-4c1c-9a10-8f0d77beaf35', 'CUSTOMER', 'customer23@example.com', '+1-678-267-9416', 'HASH', 'Scott Brooks', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('730d3924-159d-4c1c-9a10-8f0d77beaf35', 'CUS-C024') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('679082f5-f87b-4aee-b281-feae3ee5b4e8', 'CUSTOMER', 'customer24@example.com', '001-867-895-0013x3444', 'HASH', 'Bobby Clark', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('679082f5-f87b-4aee-b281-feae3ee5b4e8', 'CUS-C025') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('92467be5-2829-42a3-b13d-b165417d31fe', 'CUSTOMER', 'customer25@example.com', '(295)585-2618', 'HASH', 'Jeff Conley', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('92467be5-2829-42a3-b13d-b165417d31fe', 'CUS-C026') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('a3528cd2-3280-499c-b6bc-04b57fb0e040', 'CUSTOMER', 'customer26@example.com', '991.273.7604', 'HASH', 'Daniel Soto', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('a3528cd2-3280-499c-b6bc-04b57fb0e040', 'CUS-C027') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('d713d254-8d30-4167-ad84-b1052b42ca76', 'CUSTOMER', 'customer27@example.com', '869-549-4228x6757', 'HASH', 'Linda Hurley', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('d713d254-8d30-4167-ad84-b1052b42ca76', 'CUS-C028') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('f3ee0d29-4795-4815-a5ec-96aeaf24e4b6', 'CUSTOMER', 'customer28@example.com', '(463)416-7027', 'HASH', 'James Morton', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('f3ee0d29-4795-4815-a5ec-96aeaf24e4b6', 'CUS-C029') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('345ae931-45ac-47b9-b71f-de9d5066e333', 'CUSTOMER', 'customer29@example.com', '726.769.7893x86336', 'HASH', 'Heather Moore', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('345ae931-45ac-47b9-b71f-de9d5066e333', 'CUS-C030') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('d539f172-bfe4-4194-8a31-11d834c8b008', 'CUSTOMER', 'customer30@example.com', '531-353-6421x01707', 'HASH', 'Michael Tanner', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('d539f172-bfe4-4194-8a31-11d834c8b008', 'CUS-C031') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('a67df45f-ea44-409e-978a-c3077b5c62f0', 'CUSTOMER', 'customer31@example.com', '+1-426-983-5021', 'HASH', 'Shawn Morgan', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('a67df45f-ea44-409e-978a-c3077b5c62f0', 'CUS-C032') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('7f996c13-fef5-4116-9c64-3847af14fceb', 'CUSTOMER', 'customer32@example.com', '+1-832-601-7564x393', 'HASH', 'Derrick Carter', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('7f996c13-fef5-4116-9c64-3847af14fceb', 'CUS-C033') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('5803c767-587c-4d81-9554-f9bdc672762d', 'CUSTOMER', 'customer33@example.com', '001-836-558-1687', 'HASH', 'Erin Hamilton', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('5803c767-587c-4d81-9554-f9bdc672762d', 'CUS-C034') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('3878efb3-ac1d-4607-9841-f1a05590022f', 'CUSTOMER', 'customer34@example.com', '(260)443-5182', 'HASH', 'Victor Harper', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('3878efb3-ac1d-4607-9841-f1a05590022f', 'CUS-C035') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('6e28cdab-b940-4c14-8bd0-e172daf13967', 'CUSTOMER', 'customer35@example.com', '+1-571-264-1644x5735', 'HASH', 'Nancy Solis', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('6e28cdab-b940-4c14-8bd0-e172daf13967', 'CUS-C036') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('9c4c65e1-7440-4022-b989-166e08ca62d2', 'CUSTOMER', 'customer36@example.com', '(619)820-9477x80920', 'HASH', 'Daniel Lewis', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('9c4c65e1-7440-4022-b989-166e08ca62d2', 'CUS-C037') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('ace54682-368f-4150-8c43-ed34cc60c3d3', 'CUSTOMER', 'customer37@example.com', '001-976-748-6100', 'HASH', 'Erica Reeves', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('ace54682-368f-4150-8c43-ed34cc60c3d3', 'CUS-C038') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('76fef5b5-ea32-4047-91ff-79d5f497ba98', 'CUSTOMER', 'customer38@example.com', '+1-625-788-8416x288', 'HASH', 'Randall Gates', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('76fef5b5-ea32-4047-91ff-79d5f497ba98', 'CUS-C039') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('d7b3a696-a422-43d9-8b96-0b187a22f610', 'CUSTOMER', 'customer39@example.com', '9183085636', 'HASH', 'Ronnie Leblanc', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('d7b3a696-a422-43d9-8b96-0b187a22f610', 'CUS-C040') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('753113b2-3020-41ae-9e7d-f8448c2978e1', 'CUSTOMER', 'customer40@example.com', '(966)465-9469x6422', 'HASH', 'Kristen Sampson', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('753113b2-3020-41ae-9e7d-f8448c2978e1', 'CUS-C041') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('364161a5-3e6b-43cd-addc-4aeac4be1e1c', 'CUSTOMER', 'customer41@example.com', '229-317-2952', 'HASH', 'Debra Stephens', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('364161a5-3e6b-43cd-addc-4aeac4be1e1c', 'CUS-C042') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('1e1ffb55-177f-47bb-9b55-1ee1f75c9813', 'CUSTOMER', 'customer42@example.com', '945.538.3461x112', 'HASH', 'Kimberly Burke', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('1e1ffb55-177f-47bb-9b55-1ee1f75c9813', 'CUS-C043') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('0eff09cc-64c8-42f2-bde4-c1beeb2049ce', 'CUSTOMER', 'customer43@example.com', '978.545.2565', 'HASH', 'Angela Benson', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('0eff09cc-64c8-42f2-bde4-c1beeb2049ce', 'CUS-C044') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('6103172c-e63e-43ea-8351-3b10ccce0004', 'CUSTOMER', 'customer44@example.com', '(205)700-6311x3303', 'HASH', 'Mary Walsh', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('6103172c-e63e-43ea-8351-3b10ccce0004', 'CUS-C045') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('8d56a5be-25d6-4d65-a7bf-8b8d09809c3c', 'CUSTOMER', 'customer45@example.com', '001-732-848-0640', 'HASH', 'Denise Porter', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('8d56a5be-25d6-4d65-a7bf-8b8d09809c3c', 'CUS-C046') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('013e01ac-8a38-4082-863e-b59e860c4d7d', 'CUSTOMER', 'customer46@example.com', '264-861-7041x87308', 'HASH', 'William Andrews', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('013e01ac-8a38-4082-863e-b59e860c4d7d', 'CUS-C047') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('afb9f238-da4a-4ebb-91ba-7ed113ec6e90', 'CUSTOMER', 'customer47@example.com', '+1-504-575-5055x38922', 'HASH', 'Jerry Navarro', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('afb9f238-da4a-4ebb-91ba-7ed113ec6e90', 'CUS-C048') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('cdae9859-b5a6-4e95-9f26-8042e60ad1c5', 'CUSTOMER', 'customer48@example.com', '+1-747-853-0720', 'HASH', 'Brian Flynn', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('cdae9859-b5a6-4e95-9f26-8042e60ad1c5', 'CUS-C049') ON CONFLICT DO NOTHING;
INSERT INTO users (id, role, email, phone, password_hash, full_name, status)
VALUES ('445bd67e-ead3-4553-a9e9-0a156a68e61e', 'CUSTOMER', 'customer49@example.com', '001-306-676-2129x5467', 'HASH', 'James Brooks', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO customer_profiles (user_id, customer_code)
VALUES ('445bd67e-ead3-4553-a9e9-0a156a68e61e', 'CUS-C050') ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('d8498a6b-a6b0-43bb-aa57-f8996b656c21', 'P_133471839', 'APARTMENT', '1 PHÒNG NGỦ BAN CÔNG - MỚI 100% DTICH 50m2 NGAY LUỸ BÁN BÍCH', 'Dự án: 
Thông tin chi tiết: 🏡 CHO THUÊ CĂN HỘ #1PN 50m2 FULL NỘI THẤT – LUỸ BÁN BÍCH 🩵🩵

📍  Vườn Lài - Phú Thọ Hoà - Tân Phú 

✨ Vị trí cực thuận tiện:

✔ Full nội thất tiện nghi

✔ Không gian sạch đẹp, thoáng mát

✔ Khu vực an ninh, dân trí cao

✔ Phù hợp sinh viên, nhân viên văn phòng và tiếp viên hàng không


Hỗ trợ xem phòng 24/7', 'UNDER_OFFER', 'Quận Tân Phú, Tp Hồ Chí Minh', 50, 7500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1d17062e-e1e6-472e-8c74-a8bc8259f36d', 'd8498a6b-a6b0-43bb-aa57-f8996b656c21', 'IMAGE', 'https://cdn.chotot.com/a-n1_vFKfd69ZziDbPXWuN3Pk7etqCMT8zNFz0DosBg/preset:view/plain/de296d72d64f9ef7dad54663f83317c8-2992513543623407117.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2e70ae05-d705-4eee-9500-856fbbd0f5cb', 'd8498a6b-a6b0-43bb-aa57-f8996b656c21', 'IMAGE', 'https://cdn.chotot.com/WTL1Pto7q9yQ7Iw6i_UEnOpHmUfq-EGyELo-psp32Ug/preset:view/plain/e2fbc8f1a14c600a6072328e0ee25f7e-2992513544101314615.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('73f25262-c47f-49fb-bd77-bf22b7b0dd21', 'd8498a6b-a6b0-43bb-aa57-f8996b656c21', 'IMAGE', 'https://cdn.chotot.com/xZJzgbSKj6A0KNikX82AyxVYb8krOs9kFpqXmSm2RdU/preset:view/plain/b56215cfe8dd41cb2bf37b59c0329e1b-2992513544045269658.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f87c52e5-cbea-4719-94ff-505585b8b9ec', 'd8498a6b-a6b0-43bb-aa57-f8996b656c21', 'IMAGE', 'https://cdn.chotot.com/cvdq1o--ShyR4JR7XmYP5mKsLCDbhEMkhGdBYtsjDzI/preset:view/plain/2756e53837938328745eab1183c31690-2992513544190781847.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('91c9f03b-10b3-4a93-bb3b-02ceddbb6de6', 'd8498a6b-a6b0-43bb-aa57-f8996b656c21', 'IMAGE', 'https://cdn.chotot.com/J00ps7YehhcZORiTOseT0WEmm4FjJgl8lWW6RjacKWI/preset:view/plain/b7f6bf1f0e6793fb44a93eb522ac5275-2992513544115782894.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dd8dd0f8-de2d-490d-8b37-191a582bd467', 'd8498a6b-a6b0-43bb-aa57-f8996b656c21', 'IMAGE', 'https://cdn.chotot.com/yBZoEp5Rj9nU2nkTgObC8I8dYKW6yndqAeARfDmfduo/preset:view/plain/e7e3a137f7b84c2671643d69774722e5-2992513544436595925.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4a52e1be-391d-4d81-9edb-22d1f61d0667', 'd8498a6b-a6b0-43bb-aa57-f8996b656c21', 'IMAGE', 'https://cdn.chotot.com/o96yL1gtS3Fu68YV5lyLDPTXuewLo0xVIP2sJren_8g/preset:view/plain/ad429a1eff2b032aa9965c3a800f7177-2992513544065580198.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3ce723f6-8ad3-432c-a115-fa0c9d8cfafc', 'd8498a6b-a6b0-43bb-aa57-f8996b656c21', 'IMAGE', 'https://cdn.chotot.com/20gU9NNteoMCIf31ceVKf_ZynCC6_EDxJqEz2Fav6OQ/preset:view/plain/79c2457140e2df1d804c513b357e83a3-2992513544267438791.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('69ade696-07d7-4017-95cb-ac5245bca2af', 'd8498a6b-a6b0-43bb-aa57-f8996b656c21', 'IMAGE', 'https://cdn.chotot.com/MVx5zZvz3Q_bNgdvLn_ihm8j-_-AEDQ4MmJjJMjC1fQ/preset:view/plain/43f666924eec39b8d9de6521d8b345e9-2992513544717725449.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7891bf06-c0e9-4e46-99c6-03b4ff017cbd', 'd8498a6b-a6b0-43bb-aa57-f8996b656c21', 'IMAGE', 'https://cdn.chotot.com/qubFSGVbBqaQ7noafcU1Q59b0UWUI5nJyxiuisK8oQE/preset:view/plain/945364760bdb5da3d44de5a733abe32d-2992513544421287909.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f7301e09-19da-4453-b076-2d3e78569f9f', 'd8498a6b-a6b0-43bb-aa57-f8996b656c21', 'IMAGE', 'https://cdn.chotot.com/S74_fn6g-9uoPfd3JLS9SgaMFGg_xcMmfAe3fsinikE/preset:view/plain/06c77ef845b41557f3fd986339fb0eed-2992513544626495383.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('883864b0-df89-46aa-b233-ce593ef6b1c6', 'd8498a6b-a6b0-43bb-aa57-f8996b656c21', 'IMAGE', 'https://cdn.chotot.com/JJilffuQ7tAMLEsyCo2i4AnWHu2sszzBBPsUEhYPUug/preset:view/plain/f4877b1765242bdcb028bd668de5e0d6-2992513544495793148.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('d9c22b0e-0b7b-4592-97aa-841aab32000f', 'P_133941386', 'APARTMENT', 'Căn hộ 3 phòng ngủ , 2 wc nhà mới 100%', 'Dự án: 
Thông tin chi tiết: THÔNG BÁO DỰ ÁN MỚI 📣

- 📍Địa chỉ: 433 Tân Sơn, An Hội Tây, Gò Vấp
- Quy mô: thang máy , 11p
- Nội thất: 
3pn: 3 giường, 3 máy lạnh, kệ bếp, nước nóng lạnh
2pn: 2 giường, 2 máy lạnh, kệ bếp, nước nóng lạnh
Sảnh vp: máy lạnh, nước nóng lạnh
Studio: máy lạnh, tủ đồ, giường, kệ bếp

Chính sách: 
• Điện 4k/kwh.
• Nước 100k/người/tháng.
• Gửi xe 120k/xe/tháng.
• Phí dịch vụ 110k/người/tháng
Không pet, nhận xe điện', 'SOLD', 'Quận Gò Vấp, Tp Hồ Chí Minh', 40, 11000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ef0465a4-c79c-4b3f-bb3a-7ef1f1a25b86', 'd9c22b0e-0b7b-4592-97aa-841aab32000f', 'IMAGE', 'https://cdn.chotot.com/9ep06Z7QwpRSl6Hw-MJGl6ly2MclA-v-WXG9AzveQg4/preset:view/plain/e496d219bddb2dda6fe9486eedee7a4d-2996125274449483929.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('56367d6f-a5c9-4fde-856c-6047a758e464', 'd9c22b0e-0b7b-4592-97aa-841aab32000f', 'IMAGE', 'https://cdn.chotot.com/uTDK3qid-WPFPMN3oa2JYLL1QIuAIRjQc1H_ahyAHZk/preset:view/plain/39ad909d6671fb2fdbd68f5f367a5875-2996125274134301049.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('270f1cda-929d-40a3-a6d1-aa92aeb1b8ab', 'd9c22b0e-0b7b-4592-97aa-841aab32000f', 'IMAGE', 'https://cdn.chotot.com/TYUtymL2z--DQVglHB24TImP_WC1iiuQZeSzUzoe3rA/preset:view/plain/bffcd3f0a2b2c99ed629d889ba5875d2-2996125274783154664.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f287088b-5019-4dff-9d56-32304590f481', 'd9c22b0e-0b7b-4592-97aa-841aab32000f', 'IMAGE', 'https://cdn.chotot.com/y4KMzJbzmYLs9kd5IxJq4C-svP8j5ra7-VsFvENHn-k/preset:view/plain/7e0ee9e93bb041ee7a6e133fdd2cc563-2996125274823185407.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9d128b18-9983-4cc7-bce3-20719b01a89b', 'd9c22b0e-0b7b-4592-97aa-841aab32000f', 'IMAGE', 'https://cdn.chotot.com/qlaArw_iyptiz1BlSp7SgBziratpLpF2Mf4slkeUQY0/preset:view/plain/9f034edfddd922266ddee531e9879aac-2996125274850151682.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('51e307f6-a5f4-44cb-9fd2-e6d09418572c', 'd9c22b0e-0b7b-4592-97aa-841aab32000f', 'IMAGE', 'https://cdn.chotot.com/IrSAzkg0wNrMRxsQJcidCqv3zY6OzKg5LCjmEgIz5qM/preset:view/plain/4491d10a139ae1539ea1f40c1ad82e59-2996125274665649809.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f185729c-898e-47c0-9263-730a14976484', 'd9c22b0e-0b7b-4592-97aa-841aab32000f', 'IMAGE', 'https://cdn.chotot.com/ZMjryO-LrNUNLYA0qAWXZ9n4wbyVNv8lzSAyXtd-yPI/preset:view/plain/32be34a150870d0cc5e615bf38389b56-2996125274676175908.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cc314537-f2f6-495e-b1d4-8a93025fcabb', 'd9c22b0e-0b7b-4592-97aa-841aab32000f', 'IMAGE', 'https://cdn.chotot.com/YpWP6PykMImigfwhfVfOuol3uFHSqz9NWF6z685gf4U/preset:view/plain/8c27695ccdcf74799e9d72795edd7c14-2996125274694426712.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d944506b-2836-4926-9128-6a433fa5523b', 'd9c22b0e-0b7b-4592-97aa-841aab32000f', 'IMAGE', 'https://cdn.chotot.com/M-2hutcZBIfWYYw8SfZV-Cucn5Y0SwysI7mnw1jzyU0/preset:view/plain/2da16796b952a2791401fec7a288f416-2996125274751211601.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('59e4965d-2919-437f-b097-a82827c008fd', 'd9c22b0e-0b7b-4592-97aa-841aab32000f', 'IMAGE', 'https://cdn.chotot.com/yCtvvyeFwww7Ei02egt97zq9ktDEbDRCCJFRMK_OfvU/preset:view/plain/e15d264d6ac1060bca01c45437e5d06e-2996125274684697527.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7e4893b9-59f5-476b-b19f-be251e113cfb', 'd9c22b0e-0b7b-4592-97aa-841aab32000f', 'IMAGE', 'https://cdn.chotot.com/RQKI0ALZ3yCtKDcFB056QEXwK17l2yLt_lcnZ6Sasvg/preset:view/plain/cdb3f1e23fb64220f8d41ae2f20887eb-2996125274690891355.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6931f878-6934-41bb-ac50-b82f3ecd3e2e', 'd9c22b0e-0b7b-4592-97aa-841aab32000f', 'IMAGE', 'https://cdn.chotot.com/Au7Jx_uIypyzFINhGkNefiCRRCDGrGvavC11OmsHE3I/preset:view/plain/fe5c0979a4cd861077bb746f4fa04ead-2996125274917266605.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('c9f50e5e-124e-4ec2-87de-8d2559a299a3', 'P_131743123', 'APARTMENT', 'CHDV studio/1PN ban công, tách bếp, full NT, phòng rộng📍LBB-Âu Cơ', 'Dự án: 
Thông tin chi tiết: 🍐Địa chỉ: Luỹ Bán Bích - Âu Cơ, Tân Phú 

🌸 Dạng phòng: studio giá 6tr5, 1PN tách bếp giá 7trX

🐾 𝐓𝐢𝐞̣̂𝐧 𝐢́𝐜𝐡 𝐭𝐨𝐚̀ 𝐧𝐡𝐚̀:
•Toà nhà thang máy, hầm xe rộng
•Giờ giấc tự do, ra vào vân tay 
•Hệ thống PCCC đạt chuẩn
•Camera an ninh 24/7 

➖➖➖➖➖➖➖➖➖➖➖➖➖➖
☎️ Liên hệ 24/7 (call/zalo/messenger) - Gia Ân để được tư vấn và hỗ trợ xem phòng ☺️', 'UNDER_OFFER', 'Quận Tân Phú, Tp Hồ Chí Minh', 45, 6500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e2ea80bb-19ba-47d6-a550-c53f944f99a6', 'c9f50e5e-124e-4ec2-87de-8d2559a299a3', 'IMAGE', 'https://cdn.chotot.com/-Kbp_Y47NSURypOL04VLH1MtHtyfDZHYnQ3GCKWOK5I/preset:view/plain/6487eeeaa7469c3f2c4c340f1d4015e2-2991972511809266041.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f3f90b39-8afa-4386-bc6b-c23bdd127e8e', 'c9f50e5e-124e-4ec2-87de-8d2559a299a3', 'IMAGE', 'https://cdn.chotot.com/dKtQnPIHSc3zH2ZZzBfvL4ki6ix0rqYz-tb6LE8zH2Y/preset:view/plain/07684ad70e0f4a075d4dead6e6aedf39-2991972512419158180.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('509aca61-9584-4e01-a258-1cb9ba974e87', 'c9f50e5e-124e-4ec2-87de-8d2559a299a3', 'IMAGE', 'https://cdn.chotot.com/r6Un4oSYjHgmN-MoySSbwxof_yGhVTqEVRCT1r8gyjs/preset:view/plain/770bc4f36621a7d84cbf790b42b518be-2991972511874429660.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('941747ea-645b-4c1b-9673-a397a367a22e', 'c9f50e5e-124e-4ec2-87de-8d2559a299a3', 'IMAGE', 'https://cdn.chotot.com/VTBCAU7K_WbXheIx3_X_eCn2D_hqFEZGHJzvIIGqPs8/preset:view/plain/f5452d5447ce5cf7d880f9e56e1a102f-2991972512016429030.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('237c7337-3f14-4ac3-a7bb-0ff7f12adb6d', 'c9f50e5e-124e-4ec2-87de-8d2559a299a3', 'IMAGE', 'https://cdn.chotot.com/b5hSviZlCva-w6vFtNP7dVjvTp54xivjvy9LlMarT-E/preset:view/plain/a939489ad4a536977c5eb6ac5ac932cc-2991972511905332377.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('121f0d8c-7936-4750-8f3e-c3851f85e7eb', 'c9f50e5e-124e-4ec2-87de-8d2559a299a3', 'IMAGE', 'https://cdn.chotot.com/XRuRDuADq0hg-PLDvbtw0yLXlk31_IygtdPxXfImYrI/preset:view/plain/cf9f821bd02349e3152a82e7d58ef38f-2991972512243534964.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0abe71a5-c890-48db-ae85-41fa3ece26ce', 'c9f50e5e-124e-4ec2-87de-8d2559a299a3', 'IMAGE', 'https://cdn.chotot.com/xwXiPsPP-BLe_WvnnD2xuOTrBWsWFD1d05hXaUe8FYM/preset:view/plain/f9427f548b3800c5b02ff132a5a674ac-2991972511718822721.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('538d6369-439d-4c13-b5ed-f7ffccaaa310', 'c9f50e5e-124e-4ec2-87de-8d2559a299a3', 'IMAGE', 'https://cdn.chotot.com/SpQKPFPvjYxRfjrDhSReR_-HoVn-yml8Mz7GtR3-EoE/preset:view/plain/56027a22727f12a265d6c7d498c1e553-2991972512270270056.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6b94e1f9-62f3-4b9b-be35-d9427417aefd', 'c9f50e5e-124e-4ec2-87de-8d2559a299a3', 'IMAGE', 'https://cdn.chotot.com/OfdW-EEVCfWODIULznMDcfXxBpUJdCtL590OqMaGxtQ/preset:view/plain/9e5e0a82b3171ed988f217aeddf7bde0-2991972511220213522.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a6ac48a8-69e5-4ef7-9ccf-96fdd97c1c85', 'c9f50e5e-124e-4ec2-87de-8d2559a299a3', 'IMAGE', 'https://cdn.chotot.com/zZbd4bFAwxPNVsvltSTEgeb_dcegYjXOm6XJNeKaPwo/preset:view/plain/89607d6c6a7b71fbc98f115b2a5fa787-2991972511110469796.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('accc6b98-d086-40e4-9630-0995b049cd25', 'c9f50e5e-124e-4ec2-87de-8d2559a299a3', 'IMAGE', 'https://cdn.chotot.com/yx4o5uJVtKGV0Psy69FSiPi8EzXN0e_d6iBzHnfjlT0/preset:view/plain/65b7d398d9aed90574d0a59ed09b8a0d-2991972511119625146.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3975d50f-412f-4c97-abed-e8826885c2a4', 'c9f50e5e-124e-4ec2-87de-8d2559a299a3', 'IMAGE', 'https://cdn.chotot.com/QnANKKafUVINGo_66DM72dZiLO2ojjIKC3ZJ6lTW_oU/preset:view/plain/a0737ae04a38bc4c22bb3ac0b386c8db-2991972511089988088.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('6ba642f2-4bd1-401c-876e-229056c0cee6', 'P_130529479', 'APARTMENT', 'Bán căn 1PN+ - 54m2- The Privia View Công Viên tầng Trung - Giá bao sổ', 'Cần bán The Privia 1PN+ (54m²) - Diện tích thông thủy 50,1m2

1) Tầng 10, view trực diện công viên thoáng mát cả ngày.

2) Nhà mới 100%, full nội thất cơ bản từ CĐT - Có rèm

3) Đã có sổ hồng

4) Giá bán đã bao gồm thuế phí ra sổ', 'SOLD', 'Quận Bình Tân, Tp Hồ Chí Minh', 54, 3650000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a59acf48-bf75-45fd-8bc7-400fc249ba9f', '6ba642f2-4bd1-401c-876e-229056c0cee6', 'IMAGE', 'https://cdn.chotot.com/Cydx93MtzODWFsZzW20edLbo-3srQtopNxeujL5SX6o/preset:view/plain/06b637e74ed41947d408de38e35d524e-2968846116222897622.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f9ff09a6-0815-41f9-85b6-5fadbe436103', '6ba642f2-4bd1-401c-876e-229056c0cee6', 'IMAGE', 'https://cdn.chotot.com/t15iyB1Mg2ntb3kmhqc3AmuZOxcfKtEgXikjI1m_9N4/preset:view/plain/b046abe00b8cafaf2f6375dd71270e26-2968846120531419409.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('59080815-5d4e-492a-81e0-9a05162fa10f', '6ba642f2-4bd1-401c-876e-229056c0cee6', 'IMAGE', 'https://cdn.chotot.com/nMrYJHFmuAdjtm5H-w_LyLCvLLPqaTU65YImbn53Gtw/preset:view/plain/8689371e3e98241359225f21dad2bd50-2968846126759316950.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0b2bb5ea-e667-4b7e-9119-518bad35ac75', '6ba642f2-4bd1-401c-876e-229056c0cee6', 'IMAGE', 'https://cdn.chotot.com/mEJwXSMwbu7g85Hr_FiqgAtDVbypmht5fyuT6qY4oss/preset:view/plain/4397ce0cdb24aeb17810b8ca7a538ff0-2968846129643503389.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3ba07542-3a92-4989-9763-52900e930244', '6ba642f2-4bd1-401c-876e-229056c0cee6', 'IMAGE', 'https://cdn.chotot.com/8-3ziKiLQ5l4lyxqKH_PU6e5XTvbhQLri1aglf_irU4/preset:view/plain/d50ce236a3de2b89d52dc10e3420c413-2968846407414943190.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('fe840cab-73c5-4889-ad7c-ae103a985d72', 'P_133941382', 'APARTMENT', 'Bán Căn Hộ Akari City 2 Phòng Ngủ 2 Nhà Vệ Sinh 80m2 full nội thất', 'Dự án: 
Thông tin chi tiết: 𝐁𝐚́𝐧 𝐧𝐡𝐚𝐧𝐡 𝐜𝐚̆𝐧 𝐀𝐤𝐚𝐫𝐢 𝐏𝐡𝐚𝐬𝐞 𝟐 
🔺 DT: 80m2 | 2PN - 2WC 
🔺 Giá chỉ: 4.7 tỷ  full (có sổ)
🔺 Hướng Đông Bắc - nhìn về Quận 1
🔺 Nội thất: Full cao cấp (đầu tư 250 triệu)
🔺 Ưu tiên khách mua cho thuê, sẵn hđ thuê 15 triệu/ tháng
-Akari City nằm tại 77 đại lộ Võ Văn Kiệt, phường An Lạc, quận Bình Tân, TP.HCM -Dự án có nhiều tiện ích nội khu như hồ bơi, gym, siêu thị, nhà hàng, café, khu vui chơi trẻ em, mảng xanh và không gian sinh hoạt cộng đồng.  -Phí quản lý: 13.500 đồng/m² với Giai đoạn 1 , Giai đoạn 2 đang miễn phí -Phí gửi xe có bảng riêng theo từng loại xe và thời điểm.  -Điện nước cư dân thanh toán theo thực tế sử dụng.', 'UNDER_OFFER', 'Quận Bình Tân, Tp Hồ Chí Minh', 80, 4700000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('840f4ef2-53a0-43f4-99fb-d26c145d576f', 'fe840cab-73c5-4889-ad7c-ae103a985d72', 'IMAGE', 'https://cdn.chotot.com/zq42YyQuDgbTauDNlCR3U2hJiJRktjBsqx-xUtfi994/preset:view/plain/af055dec7ea4c2abaae3945b36a1e670-2996125458972552795.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fe888e08-ba78-473f-8e82-6dee12a466c7', 'fe840cab-73c5-4889-ad7c-ae103a985d72', 'IMAGE', 'https://cdn.chotot.com/mj1cg5dXuOtG5R168iNgMbyOEUfnxG9L4qDKp-VE2xc/preset:view/plain/8172b18ad5fd3d7ff8e7a09d6022b277-2996125459135501608.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9e230bc0-5547-49fa-b113-51dfa68d680f', 'fe840cab-73c5-4889-ad7c-ae103a985d72', 'IMAGE', 'https://cdn.chotot.com/KP_9f1rrCexsbYd5sW58PmcVnU6nhISsJVAL21Hdd1A/preset:view/plain/60d4d7366d846f57b3ad054387d2ac60-2996125459478963878.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cfff78be-2f07-4f7e-bcf6-0ae584e4345e', 'fe840cab-73c5-4889-ad7c-ae103a985d72', 'IMAGE', 'https://cdn.chotot.com/7MyiS8_bzH6svhxANQkQE9s-yiix2P4MIm_zNSO38qY/preset:view/plain/4b932b963f2af7fda71b01eae6e3ad93-2996125459236165785.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('91012840-855a-4364-9429-5a28ff42d602', 'fe840cab-73c5-4889-ad7c-ae103a985d72', 'IMAGE', 'https://cdn.chotot.com/GVGLgNMuk7LO7wdc0ity-gN6BRpXEKdd_Whyj2lSV0w/preset:view/plain/dc99c1f071ddee2de712e571dd09b030-2996125459308070372.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9f8a956f-4626-46a1-baad-4b5e659c270d', 'fe840cab-73c5-4889-ad7c-ae103a985d72', 'IMAGE', 'https://cdn.chotot.com/cSEAPGWqj7fsdM-OqtHHmpEvLcmo7QtKplif-e2Z2sM/preset:view/plain/fc3a30976f696f31325f7752b888f7a0-2996125459876860927.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8b00b233-9e35-4b86-be83-20e8463fb50a', 'fe840cab-73c5-4889-ad7c-ae103a985d72', 'IMAGE', 'https://cdn.chotot.com/CPaDgZB2ygBwo22ty5E0wSlkAv07b6OpjhBZK59_uB4/preset:view/plain/7918b2983dd3221745b8115905e0ee09-2996125459157109113.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9ee73909-c1ae-4774-9a99-0128d274ea41', 'fe840cab-73c5-4889-ad7c-ae103a985d72', 'IMAGE', 'https://cdn.chotot.com/YwWJ7R5GNF4UMHDzwzCh4Muk0vMh8PVGYjSpCwYYhuY/preset:view/plain/992b943347496d5a49fda656146f6bf3-2996125459502533685.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('af885a3c-3884-4df6-a4f7-27540914dc4f', 'fe840cab-73c5-4889-ad7c-ae103a985d72', 'IMAGE', 'https://cdn.chotot.com/2egO4GG4BxzL4mNzHnSkR1daKWMCL_S43S7XBKwtcjo/preset:view/plain/e4f61064bf03a94baf661c9096fc9547-2996125459517068952.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('74900b93-2b4c-4d15-aa97-374919ecbb3c', 'fe840cab-73c5-4889-ad7c-ae103a985d72', 'IMAGE', 'https://cdn.chotot.com/MqY6DoTMDosjTb16ORKi190_z9YGhxtF_guHctGPznQ/preset:view/plain/223130a87d00b74a556109d6a8c14604-2996125459786039784.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f6f2a74f-ac36-4648-a644-835ae949fadb', 'fe840cab-73c5-4889-ad7c-ae103a985d72', 'IMAGE', 'https://cdn.chotot.com/YNBwJEZ0lGdm_YeZR9DkUNB6YrfNuy6jEDQW5JoyL2k/preset:view/plain/53d83a7477147e50eba0132c502d1d78-2996125459534251665.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e70ffc92-973a-431c-8661-99b334248a57', 'fe840cab-73c5-4889-ad7c-ae103a985d72', 'IMAGE', 'https://cdn.chotot.com/gApIq1IMa5hP01pAzbF1_l7jpkB-AIy7fFhFWamWhIE/preset:view/plain/573db8af9acb1254d035a96e9ed188d1-2996125459496771672.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('024257ad-144c-40ce-98df-285e7e5372a6', 'P_133809089', 'APARTMENT', 'PASS PHÒNG BAN CÔNG FULL NỘI THẤT NGAY TỈNH LỘ 10 - TRẦN VĂN GIÀU', 'Dự án: 
Thông tin chi tiết: 🏰CĂN HỘ CHUNG CƯ MINI FULL NỘI THẤT KOLA APARMENT 

✨ TỈNH LỘ 10 - TRẦN VĂN GIÀU 

✨ 4tr2 sẵn máy lạnh tủ đồ tủ lạnh kệ bếp bàn ghệ máy nóng lạnh máy giặt riêng ban công thoáng mát

✨ Gần vị trí : ngay Tỉnh Lộ 10 , Hương lộ 2, Aeon bình Tân, chợ Bà Hom , Trần Văn Giàu

✨ Điểm nổi bật : giờ giấc tự do, không chung chủ, ra vào vân tay, sẵn nội thất

☎️*** Nguyễn Phước nhắn em để được em tư vấn và xem phòng trực tiếp', 'SOLD', 'Quận Bình Tân, Tp Hồ Chí Minh', 30, 4200000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('84bf346e-3443-48e7-a0c5-b49cec1acde5', '024257ad-144c-40ce-98df-285e7e5372a6', 'IMAGE', 'https://cdn.chotot.com/Q_uMw4i9xare8bRYwkcrJkhvg670pWP_Zj305cR_298/preset:view/plain/4c84e2bffeb7e633b4cc8b548da34ce3-2995116838034917630.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('02d98508-dfe3-4fb2-9471-0c1bf58e4d8e', '024257ad-144c-40ce-98df-285e7e5372a6', 'IMAGE', 'https://cdn.chotot.com/rkQx--rjlLE7B10Zz6C2WaCaw4wwDAH8fDSYbm9O0IY/preset:view/plain/6828065dc304420166444bb3dc88a703-2995116838082237296.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e03ef218-e5b0-473c-b0cd-3f621bce07c7', '024257ad-144c-40ce-98df-285e7e5372a6', 'IMAGE', 'https://cdn.chotot.com/OTJ4wNUkO1Dg2gzi6E45A1H_G8tnOT2Qt4n-58gMrUQ/preset:view/plain/406820bcec40b662dac35eb7573d9956-2995116838129973016.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6fbf5244-b420-4f95-a7ef-8c17e498904a', '024257ad-144c-40ce-98df-285e7e5372a6', 'IMAGE', 'https://cdn.chotot.com/7zoI9XCIr-_1It5l0Hkmj1EhPTD-fmShJAKP6tnqOAM/preset:view/plain/15ce3ac2c2fc2cf4989ff6459fb907f9-2995116838043927396.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('34afc064-7fbb-4232-b85b-88d1f97d708c', '024257ad-144c-40ce-98df-285e7e5372a6', 'IMAGE', 'https://cdn.chotot.com/b1N2d-JGlSZkqkMu8qD8Xx2z8mhvkACYxQBJwse7DOo/preset:view/plain/62b91ed6f3727491c671a0308bccdcad-2995116841236419440.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cd174c66-61bf-4a38-85e2-a75607a17efb', '024257ad-144c-40ce-98df-285e7e5372a6', 'IMAGE', 'https://cdn.chotot.com/4Im1P1QZh7L4zkIfDiQAJaRCxLsvo-G8iTyRyWzUGbs/preset:view/plain/63a977af4f63de07232a00b7c2697855-2995116838071533576.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3260932c-646b-464e-a493-d040b510b8fe', '024257ad-144c-40ce-98df-285e7e5372a6', 'IMAGE', 'https://cdn.chotot.com/w-OelBZ97-sx4RpceO2gJLI0rE3gbtKhh4WVO85l4I0/preset:view/plain/d45f1128b97747ecce7347e2aa91ce7f-2995116837961984257.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('22952742-5368-4cce-9477-0135a4ffa693', 'P_133941373', 'APARTMENT', 'CHDV Full Nội Thất Mới Nằm Ngay Mã Lò - Gần Bệnh Viện Đa Khoa', 'Dự án: 
Thông tin chi tiết: 👉 Chỉ Tính Điện Nước
👉 Cho Xe Điện
👉 Giờ Giấc Tự Do
👉 Cổng Vân Tay
☎️ Liên hệ em Thắng hỗ trợ xem phòng', 'AVAILABLE', 'Quận Bình Tân, Tp Hồ Chí Minh', 30, 4300000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d5c893c8-03e7-43b8-9acd-0324d8566eb3', '22952742-5368-4cce-9477-0135a4ffa693', 'IMAGE', 'https://cdn.chotot.com/LVI-daOUMrx128abmw25acXDLp3o2C27KBFnwOKmlQI/preset:view/plain/60072bfc57057fbff61d98486f43363c-2996125232056060281.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b37c0389-215d-439c-832d-2822b7f9eaee', '22952742-5368-4cce-9477-0135a4ffa693', 'IMAGE', 'https://cdn.chotot.com/cY6PpQLAt7m8vCaavoKZFISdPTUHfHLUEkBUzLCfWSA/preset:view/plain/3cb70381615c2f172a16075b2cab316b-2996125232762377215.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6bbf82a7-b343-43b1-8b32-a036bdd0f0a8', '22952742-5368-4cce-9477-0135a4ffa693', 'IMAGE', 'https://cdn.chotot.com/185sXqM1BhKPTdyjdxwUAQVKHc15rYokB-JmszjVA4s/preset:view/plain/c0e12a272d5d0903cc161a121256aefb-2996125232321964983.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('256ecea3-2241-4419-99ca-468b5470657d', '22952742-5368-4cce-9477-0135a4ffa693', 'IMAGE', 'https://cdn.chotot.com/brjjVsHxTVHL8ErzhmB7ZDqjYBqM7WtJEHwZls6QCFc/preset:view/plain/b658c8f0c22b08d0cf0cb5065a8d11be-2996125232975616081.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8c85d77f-59b8-4e86-8033-b252903a354c', '22952742-5368-4cce-9477-0135a4ffa693', 'IMAGE', 'https://cdn.chotot.com/rC-aufEN-VzIJj_mxRCUsjy94_r32Wj_uV43z9mToio/preset:view/plain/3e4e46bf6d90242078b7a160c44fac7f-2996125232791132313.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e58c6f9a-e5e9-42ca-8e4f-2c01c63a1372', '22952742-5368-4cce-9477-0135a4ffa693', 'IMAGE', 'https://cdn.chotot.com/9N4xnwWSZtGJ0U9vvmytxHL3FEDU5-sKPhEJihibpRA/preset:view/plain/c51f8d2261b5383fdeb8b2b92bfb04a8-2996125232740425509.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('462f954b-4d7a-4a3b-8a90-d75de2defce6', '22952742-5368-4cce-9477-0135a4ffa693', 'IMAGE', 'https://cdn.chotot.com/6VuINLvwSDoC-VSbpG2PXiAup87y34wFM7jqM3yj3AU/preset:view/plain/fc98c194c5224226e2545493c42df68e-2996125232883934244.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b9375cef-5160-4558-8e91-5cda410d8cbb', '22952742-5368-4cce-9477-0135a4ffa693', 'IMAGE', 'https://cdn.chotot.com/NVeWl2vEekODd1afZX21H8fXUJlfettUgRhe9c9ozfA/preset:view/plain/643f1c04787f230cd93fc2e4249961db-2996125233008973096.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d2f70c97-8891-4550-b6d0-73e24c0b00d8', '22952742-5368-4cce-9477-0135a4ffa693', 'IMAGE', 'https://cdn.chotot.com/gxoLDovZJiyxULxhwQPO0Z6DXbmnfOb24ga9ykop9Q0/preset:view/plain/b10038e2ae6475242a6b9ab05ca3db3d-2996125233167085147.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1d4a4f45-a578-4df5-bfd3-1116871c8ed0', '22952742-5368-4cce-9477-0135a4ffa693', 'IMAGE', 'https://cdn.chotot.com/VosHRVbArG4aHWkQygIGR8hnVOk3XvRHAuX_4koOsjI/preset:view/plain/a8d6ec1596dc92047f8d5973f231097c-2996125233047127524.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fbedaa1d-242f-4b8c-8321-e4a96bef33fd', '22952742-5368-4cce-9477-0135a4ffa693', 'IMAGE', 'https://cdn.chotot.com/yEBgFyqq8RfHZj-jbS49chDq6VYDz0jjibf2vs9AKRU/preset:view/plain/20c27266a5aafe9d092d4e529022e1a8-2996125233187332184.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('89709bb5-1c35-4517-8d13-b63eb3e948eb', '22952742-5368-4cce-9477-0135a4ffa693', 'IMAGE', 'https://cdn.chotot.com/R8U4CMyTCtdLtnFlwChvuU4aZUom-45ZvLaTXhKNMh0/preset:view/plain/db1ddc115222f5e5fc3ac1ffff2e7b47-2996125233913594344.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('38b0f4e8-b8c8-443e-a0bc-c65d368b2bee', 'P_133941351', 'APARTMENT', 'Sắp trống 2PN 2WC 90m2 Gold View NTCB nhà siêu mới, ở được trong t9', 'Sắp trống căn 2PN 2WC tại Gold View, vào ở ngay trong tháng 9 này

Gold View nhà hoàn toàn mới, chưa có ai ở
Căn nhà mới, thoáng mát, lầu cao view đẹp
Diện tích: 90m² 
Giá cố định 17tr/tháng
2 phòng ngủ.
2 phòng tắm.
Nhà đẹp, sạch sẽ, dọn vào ở ngay trong tháng 9.

Phù hợp gia đình hoặc khách cần không gian rộng rãi, tiện nghi, vị trí trung tâm.

Inbox để xem nhà thực tế và nhận thêm hình ảnh, video chi tiết.
', 'AVAILABLE', 'Quận 4, Tp Hồ Chí Minh', 90, 17000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('71ac192e-8c67-40aa-bd53-dd78eba464e2', '38b0f4e8-b8c8-443e-a0bc-c65d368b2bee', 'IMAGE', 'https://cdn.chotot.com/t511plpEXTC0uf40Pw8SjmcgsQ6hMAvCcUG8EISNgE0/preset:view/plain/71e723a8766c539b527f8c68360f12d7-2996125206571010425.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('33ae1098-b317-461d-8878-adf192ac3831', '38b0f4e8-b8c8-443e-a0bc-c65d368b2bee', 'IMAGE', 'https://cdn.chotot.com/PJN1C7jtDh34Di5mJyEf-NklXNMNvrsoWHywIjGcYM0/preset:view/plain/5a458424dc99056dd01276f3815e672d-2996125206753356727.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a2863229-eb91-4b7a-9a1c-0a1d711949b1', '38b0f4e8-b8c8-443e-a0bc-c65d368b2bee', 'IMAGE', 'https://cdn.chotot.com/m_ECYZSbRRa4-2mleVjUnCjLeZudWKZDXgT2TQ4i5H0/preset:view/plain/9f23ff9d3892cc1ab74e5bb0648cb9c8-2996125207602030246.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('359bd73b-fce5-4995-95c9-8bcd0fd2c526', '38b0f4e8-b8c8-443e-a0bc-c65d368b2bee', 'IMAGE', 'https://cdn.chotot.com/Dia2Y5Jo57nb0OUZ5ekbvunxoWeXoGauqJZhJ66JKG4/preset:view/plain/33c9ee41f8bdfde744db119a4763b1a8-2996125207550207012.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7fee4294-c567-48e0-be41-fb0159c00f02', '38b0f4e8-b8c8-443e-a0bc-c65d368b2bee', 'IMAGE', 'https://cdn.chotot.com/KScZZhM8kmymn7HKfdfCbgAE9UaOa6B0kP131NnQkEw/preset:view/plain/12ae50f48fed49dd6137aa7e3a8413dd-2996125211012695697.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8395d344-d8b2-4ad8-b6ba-c4358aca2124', '38b0f4e8-b8c8-443e-a0bc-c65d368b2bee', 'IMAGE', 'https://cdn.chotot.com/_8O4SNFlZz_GgaIvizfYKzBs7Fkpmv1hdxmmalfdRxQ/preset:view/plain/409ef253b129bfdfbc4a666d3743706e-2996125210448548863.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('53aad73b-c50c-48e4-8e1d-0b946042101b', '38b0f4e8-b8c8-443e-a0bc-c65d368b2bee', 'IMAGE', 'https://cdn.chotot.com/furril0I-yHYsjzptSaiy7XSdSaQr0af_CFkZRvB4N4/preset:view/plain/7357a56f74b8ede1521aa995451e7f53-2996125205616051684.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cbcc5183-ba7b-4fcf-a60c-6279f6996fcd', '38b0f4e8-b8c8-443e-a0bc-c65d368b2bee', 'IMAGE', 'https://cdn.chotot.com/e2I5IXQp6-D89bjI3QDeU9tBJly_CNh5Qcuwh0G1Qps/preset:view/plain/746fc47889969434b9d11042c8152f6f-2996125206612025432.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a367b915-0a26-4fae-b244-04912133c409', '38b0f4e8-b8c8-443e-a0bc-c65d368b2bee', 'IMAGE', 'https://cdn.chotot.com/NqvkPfyihIKBbHrTA4ddPq1dyYfxKKJjzfLrmGrHNMo/preset:view/plain/53619d678363eaa6aa117cdf872c0d3a-2996125209514549336.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2a7d03bd-b2ac-49ef-b453-829fb625fb45', '38b0f4e8-b8c8-443e-a0bc-c65d368b2bee', 'IMAGE', 'https://cdn.chotot.com/moZV5nvFDNoHa523FjWgXZVqt_4n1KJaPZWG7KApucA/preset:view/plain/1801cf1ceb6d1053fd392c7d047c5f10-2996125209654910757.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('80db0564-7306-4f44-b947-e85f98d381bd', '38b0f4e8-b8c8-443e-a0bc-c65d368b2bee', 'IMAGE', 'https://cdn.chotot.com/luZbso3HHtup5xBrMZgs49ovzcWWm-8IxmpdUuZ6T84/preset:view/plain/66f51d891bc220a886c2a3b2278aae2a-2996125211755301241.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f0019280-f27f-43bb-ab9c-79976df0a9a9', '38b0f4e8-b8c8-443e-a0bc-c65d368b2bee', 'IMAGE', 'https://cdn.chotot.com/GfPjYh73Q74ZBwbP87SeJE8Eci032cRuuL16930kg7w/preset:view/plain/01d79e756b867ec73b81ecbbbe7a6358-2996125212121142568.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('7f9a802c-f638-4073-a906-e60e1cd3ced8', 'P_133941345', 'APARTMENT', 'TRỐNG SẴN CĂN HỘ DẠNG 1PN, TÁCH BẾP, ĐẦY ĐỦ NỘI THẤT, BAN CÔNG RIÊNG', 'TRỐNG SẴN CĂN HỘ DẠNG 1PN, TÁCH BẾP, THIẾT KẾ SANG TRỌNG, RỘNG RÃI, ĐẦY ĐỦ NỘI THẤT, BAN CÔNG RIÊNG

📍Vị trí: Trương Văn Bang - Quận 2
 
- Full nội thất cao cấp
- Đảm bảo tốt PCCC
- Ban công riêng mặt trước
- Được nuôi thú cưng 
- Có chỗ đậu oto
- Giờ giấc tự do, ra vào vân tay
- Khu dân cư an ninh, thân thiện', 'AVAILABLE', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 40, 8300000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('69b3032d-11e7-4782-84d3-64ed1fb5082e', '7f9a802c-f638-4073-a906-e60e1cd3ced8', 'IMAGE', 'https://cdn.chotot.com/VzRgXbtfrOPhM4E5tHdsZRyCBq3I1KCu3x2A01Uuaw4/preset:view/plain/d4e1205583f0f2ac84452d107d37cd5c-2996125337952097576.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8daac59c-1d10-4bf6-bc88-4c2f1d1cbb43', '7f9a802c-f638-4073-a906-e60e1cd3ced8', 'IMAGE', 'https://cdn.chotot.com/6nzcD5UJYQRXPC45hQ4PKev5dM9ildhGnZP-8KVltg0/preset:view/plain/9c467a5feccb5e10329cc963eb200fb9-2996125338761382265.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6b9dbc9d-5355-41bf-9a14-2f2676b1c584', '7f9a802c-f638-4073-a906-e60e1cd3ced8', 'IMAGE', 'https://cdn.chotot.com/M6KCUrw8j6KaGA-_7r00j-ILPwfl9kblpd7hcryTnMs/preset:view/plain/591d641948e0976e466bd44767ae4db6-2996125338933109796.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('24994788-1e9c-4a24-9ac9-92c830e45584', '7f9a802c-f638-4073-a906-e60e1cd3ced8', 'IMAGE', 'https://cdn.chotot.com/IrmmHoR3L0va9UlgaCo6jaNhNlGzeoeKjvBmXybZB64/preset:view/plain/9c11ca550be6f3e0f1023413d716e07d-2996125339459245720.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f8c93146-b9e7-4ba4-880e-5ed7a4d73072', '7f9a802c-f638-4073-a906-e60e1cd3ced8', 'IMAGE', 'https://cdn.chotot.com/rSbRLBxeSWMrfj6P7NBhDgmwb3Jd9m-EuWlKiIxmMqE/preset:view/plain/e27c00027e0ff420d8cc44656b30aa48-2996125339998066769.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('945d150d-8b73-4593-9162-4e98fdddc76f', '7f9a802c-f638-4073-a906-e60e1cd3ced8', 'IMAGE', 'https://cdn.chotot.com/-L6siJPUG-nOkCRv_l3GOhcOAEQ01GG_RRdL6dLpJfQ/preset:view/plain/a096a558ed7eaef058029350c679fa6b-2996125339315717604.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a16a4a8f-44bb-4fdd-aebe-9b2871a24ab6', '7f9a802c-f638-4073-a906-e60e1cd3ced8', 'IMAGE', 'https://cdn.chotot.com/KFOLT_e9jtYm4MrhpiSjFPQKLxC0U5sBlk5y1p1JDnI/preset:view/plain/116309a50a9fb3f9ba8c78a48a434f18-2996125339119460440.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4a92099f-ba76-41bc-8c94-89ead66e71ef', '7f9a802c-f638-4073-a906-e60e1cd3ced8', 'IMAGE', 'https://cdn.chotot.com/e6enVQnsQ72yQITGaT_sPO9H8xlFWJV55lGriD4GwC8/preset:view/plain/35e00fd52b3b8f859a45d402a1119c35-2996125339315131391.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('955b55e6-a205-4ddf-a977-687d4bcb35e4', '7f9a802c-f638-4073-a906-e60e1cd3ced8', 'IMAGE', 'https://cdn.chotot.com/Znd7guD03n7ygWE7pUvpcNFJ1CovSjkNKQGwM0E9fnM/preset:view/plain/e2f9b2a2d58458cac2af8282cfcb1337-2996125339050475021.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('839a4cb0-fd0d-4f12-9b64-68831a4f5d96', '7f9a802c-f638-4073-a906-e60e1cd3ced8', 'IMAGE', 'https://cdn.chotot.com/b60MJUtegCDS7U8r7dBDjnzfGvFEwE8G5qLV-MXCQxI/preset:view/plain/05cbf408cf904ef79a1c25f6eb3cf933-2996125339730745497.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dba65fb9-e5d3-41e5-b4d6-2ecdf077b7ae', '7f9a802c-f638-4073-a906-e60e1cd3ced8', 'IMAGE', 'https://cdn.chotot.com/Vpg0ZHkjunRrikg5CObtn2vJO_LcBJxbMbiCqHyxccQ/preset:view/plain/c6128f2c2afc3ca0bb085086d6d6e27f-2996125339965429032.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a77a85e3-ec52-4e44-8ab8-c9b0591f4f11', '7f9a802c-f638-4073-a906-e60e1cd3ced8', 'IMAGE', 'https://cdn.chotot.com/gv21S167ot9BqBb8CO8QSAFD0VEHz6eQeAnrhm33DYk/preset:view/plain/f25ff8d481e46c29d21d366402de790f-2996125339434495579.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('7a1395f5-47e0-428d-b304-33e07abc82cd', 'P_133941344', 'APARTMENT', 'CĂN HỘ CHO THUÊ 1PN BAN CÔNG GẦN CV TAO ĐÀN CV LÊ VĂN TÁM MỚI 100%', 'Dự án: 
Thông tin chi tiết: 🥔 1PN BAN CÔNG VIEW PHỐ – NGAY VÕ THỊ SÁU, TÂN ĐỊNH 🥔

📍 Võ Thị Sáu, phường Tân Định, TP.HCM | Căn hộ 1PN với ban công view phố thoáng đẹp, full nội thất, không gian sáng và mát mẻ. Chỉ vài phút đến Công viên Lê Văn Tám, Hồ Con Rùa, chợ Tân Định, ĐH Kinh tế TP.HCM (UEH), thuận tiện di chuyển sang Quận 1, Bình Thạnh và Phú Nhuận.

Đừng ngại liên hệ bên em nếu cần tư vấn hoặc tìm phòng theo nhu cầu nhé! Bên em có đa dạng các loại phòng và căn hộ với nhiều phân khúc giá để Anh/Chị tham khảo. 🥰', 'AVAILABLE', 'Quận 1, Tp Hồ Chí Minh', 40, 7000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('acaf9e5b-5da4-4d75-a478-8a9a5c729e77', '7a1395f5-47e0-428d-b304-33e07abc82cd', 'IMAGE', 'https://cdn.chotot.com/80hvKJLOzGBMdF8j7gNPpkySGZRWPjcJ_thkjWisAlA/preset:view/plain/ed25a8567f990b9be0703165ae4f8187-2996125160401654783.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bc29a093-4006-43e7-8e8a-cd985f07fed8', '7a1395f5-47e0-428d-b304-33e07abc82cd', 'IMAGE', 'https://cdn.chotot.com/b_CNiV3kmcHRtS-46aTR-oVubDwVp3eACqrcIboLrrI/preset:view/plain/b09a2ce40e4077c19c4ae888593d8c2d-2996125161067747481.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c93f49d2-7504-481b-b91f-767ba4d01ad3', '7a1395f5-47e0-428d-b304-33e07abc82cd', 'IMAGE', 'https://cdn.chotot.com/-_17_IEZtLgmT3kk0t_0ViSOBlMYWmOxELW6hD6lMzI/preset:view/plain/1121c67f13605834f9d90bdd056c81f2-2996125161088665060.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b8a1534a-50c6-4cd3-aeb6-6cba511b12fa', '7a1395f5-47e0-428d-b304-33e07abc82cd', 'IMAGE', 'https://cdn.chotot.com/2Mh2vha_7_QkPg1ivkjweiENus4uSosOR8fGQ5-7HBw/preset:view/plain/0abb85e2a196bb1d53221942a52f792f-2996125160818428281.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9dda6045-7543-4695-8df6-29de8774d5eb', '7a1395f5-47e0-428d-b304-33e07abc82cd', 'IMAGE', 'https://cdn.chotot.com/iB-Mn5TfcC0DFLtNF7X5WeyX0rh6UIfeJZgJhzFEJPY/preset:view/plain/176e1c48665aab64fd377a55f49b884a-2996125161597468173.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('357f0430-0c37-405a-8d4f-92c95b936d8f', '7a1395f5-47e0-428d-b304-33e07abc82cd', 'IMAGE', 'https://cdn.chotot.com/qsl8wfdqK1gdMX9Sq-ZDyPMezKI51pmfstJDkThd04k/preset:view/plain/15183056e51432bfff618215dc4e8acc-2996125162812971089.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('179274a4-1cc9-4340-9c70-ebe2e22a972c', 'P_133941339', 'APARTMENT', 'Căn Hộ Studio Cửa Sổ Full Nội Thất 35m2 Lê Văn Lương, Q7 Gần TDTU', 'Dự án: 
Thông tin chi tiết: ✨ STUDIO CỬA SỔ • FULL NỘI THẤT CAO CẤP • LÊ VĂN LƯƠNG, QUẬN 7 ✨

📍 Vị trí: Lê Văn Lương, Quận 7  
✔️ Gần Lotte Mart, Phú Mỹ Hưng, Đại học Tôn Đức Thắng, Đại học RMIT, UFM. Thuận tiện di chuyển sang Quận 4 và Quận 1.

✨ Tiện ích căn hộ:
• Studio rộng rãi, cửa sổ lớn đón ánh sáng tự nhiên.
• Full nội thất cao cấp: giường, nệm, tủ quần áo, máy lạnh, tủ lạnh, bàn ghế, bếp...
• Không gian sạch sẽ, hiện đại, chỉ cần xách vali vào ở.
• Khu vực an ninh, yên tĩnh, phù hợp sinh viên và người đi làm.

💯 Căn hộ đẹp – vị trí thuận tiện – số lượng có hạn.', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 35, 5800000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ff256d21-df03-43a7-b115-a84c5b8c8df3', '179274a4-1cc9-4340-9c70-ebe2e22a972c', 'IMAGE', 'https://cdn.chotot.com/LLtg1EUUbWO2IjI_q_K4_fa6Th529SFOyHZwOGNVDyE/preset:view/plain/a848b5e98feffe385b1bb1bfe5d3427d-2996125124193110393.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dd49cb28-b38a-4c7f-b8b7-6e77c0a9a91a', '179274a4-1cc9-4340-9c70-ebe2e22a972c', 'IMAGE', 'https://cdn.chotot.com/5G51iiIQ07ecwZ-0MOXYciMiHzidTkmtnacwBqFBcpw/preset:view/plain/2b4e22841323cc57e6c0bb54b79d9e89-2996125124291040552.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('18d99284-f4fa-40c1-bfec-718f3c4d8530', '179274a4-1cc9-4340-9c70-ebe2e22a972c', 'IMAGE', 'https://cdn.chotot.com/hZoqDddJMoDBrIpxf822dkPzw1DpJJ6Ji1NLMYUl9UQ/preset:view/plain/cf2a4a15de6b701f230f6e1d8c8aba55-2996125124375517337.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f6f99c10-e264-4166-a4a1-b4f93663df2a', '179274a4-1cc9-4340-9c70-ebe2e22a972c', 'IMAGE', 'https://cdn.chotot.com/hl7_4Mnk0aLQKJCHQEuCDARingJAebBSIC3ZQrUGGZU/preset:view/plain/49390386284fccf5af4fa6addef53381-2996125124554137688.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8147f274-674c-4adf-8389-fda9c5550b68', '179274a4-1cc9-4340-9c70-ebe2e22a972c', 'IMAGE', 'https://cdn.chotot.com/77z_uODtspNuYO3QNb6BZKMyc9_5YFk38-E1Jko9KV0/preset:view/plain/e65c4cba7d8589195aa2daed3f29b6f7-2996125124614669796.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b1dfaba6-6469-407c-bacc-036fbe5131e9', '179274a4-1cc9-4340-9c70-ebe2e22a972c', 'IMAGE', 'https://cdn.chotot.com/DfWYJsZddBHtNtU0o5wlpmnGs0_uk8mdeOQHYo1aWeY/preset:view/plain/412d9c0c6691e42373efcf0d9e518443-2996125124578356151.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('273874d5-bfd3-4994-8ccc-cee8f6a638ed', '179274a4-1cc9-4340-9c70-ebe2e22a972c', 'IMAGE', 'https://cdn.chotot.com/puL5j0FhN3uZgDP_W_pTtJcceBJN3JK-Fh-HB3s1L9Q/preset:view/plain/b8df3b034ac409a0f9a507adf663a991-2996125125001597951.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('af5eb737-2c80-470b-9b91-ac51540202fb', '179274a4-1cc9-4340-9c70-ebe2e22a972c', 'IMAGE', 'https://cdn.chotot.com/0Je_i-ousjj1dW8iDyXgscStJvvdaZjvN0RvRkrKYrA/preset:view/plain/101b71a4997e9ce3ab3933b8721e6794-2996125125181610065.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('998703af-171e-4339-8535-022e810ef7d2', '179274a4-1cc9-4340-9c70-ebe2e22a972c', 'IMAGE', 'https://cdn.chotot.com/eLFfQOwdKf-FS8qacAnE7yYEhrxKDDIaYgeDMYFFryQ/preset:view/plain/bcea17f7bba3540170b3fdcbc8cd541e-2996125124804518948.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('fc91e064-c083-418e-8928-69bf49db9dc8', 'P_133941334', 'APARTMENT', 'CHO THUÊ CĂN HỘ MINI FULL NỘI THẤT ĐI BỘ QUA CAO ĐẲNG PASTEUR - QUẬN 6', 'Dự án: 
Thông tin chi tiết: KHAI TRƯƠNG PHÒNG GÁC MỚI XÂY - ĐI BỘ CAO ĐẲNG PASTEUR - VÒNG XOAY AN LẠC - AEON BÌNH TÂN🔥

- Nhà mới 100% chưa qua sử dụng chỉ từ 3🍠2 có phòng vào ở ngay, có cả dạng ban công để lựa chọn chỉ 4🍠1

- Toà nhà giờ giấc tự do không chung chủ, cổng vân tay an ninh 24/7 đường lớn oto thoải mái

- Vị trí cực tiện lợi có thể đi bộ sang CĐ Y Dược Pasteur chỉ 300m. Aeon Bình Tân 5 phút đi xe - CĐ Quốc Tế 6p đi xe

Call/Zalo: để được tư vấn sớm nhất — tại Cao đẳng Y Dược Pasteur.', 'UNDER_OFFER', 'Quận Bình Tân, Tp Hồ Chí Minh', 28, 3200000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('25cd7634-3d5b-4bd4-91c6-68e8ce7fd464', 'fc91e064-c083-418e-8928-69bf49db9dc8', 'IMAGE', 'https://cdn.chotot.com/d24_hH6gann1BNvGiINHU54iMG8m01wE_MuapWulEro/preset:view/plain/18c42071761a7eec41b18f8ea686dad0-2996125119377983865.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('02f31bc5-9f15-48a6-b7bc-6f42fd7664d9', 'fc91e064-c083-418e-8928-69bf49db9dc8', 'IMAGE', 'https://cdn.chotot.com/aCu33VHlEFne2oE_UtcbvwRtEJ0z1UCa5haPC_fra8A/preset:view/plain/fc95905e0901e515a09c338bea428e2b-2996125119418967076.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('567059ee-08fe-485f-bb8f-16c0a16457ea', 'fc91e064-c083-418e-8928-69bf49db9dc8', 'IMAGE', 'https://cdn.chotot.com/-AGMh7lRmve60RoyhY60nqiZz4wzAhT8IKor1upYTsc/preset:view/plain/71bd02e98f39c5a82ca9f2bc18700c79-2996125119494068305.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1fb18b72-682d-4686-a474-54580ecc0196', 'fc91e064-c083-418e-8928-69bf49db9dc8', 'IMAGE', 'https://cdn.chotot.com/gHHd1XAPxXaC6TvkP1af-y0PE1seOFvpL02f3L9PD_4/preset:view/plain/ddb1784cacb78b64519d69d529e4ed7d-2996125119621570648.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f24a1bb2-ebc3-478d-84f1-2047cf580d66', 'fc91e064-c083-418e-8928-69bf49db9dc8', 'IMAGE', 'https://cdn.chotot.com/qbJ-Ow_iNu2qtBZvQXe-XFT66sR_NaY3flIEYi7Oq4k/preset:view/plain/a049eaa3d206cf6d9a3724c855436c22-2996125120373468763.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('82b7938b-d6f6-461d-85e8-75e33273cfd2', 'fc91e064-c083-418e-8928-69bf49db9dc8', 'IMAGE', 'https://cdn.chotot.com/vHZlGHmig7ZSynEa6RqZszOLLhbd32Fgc2EivDvQDdk/preset:view/plain/6955329f5abfdecc128c6b92452b3498-2996125120365525729.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9261d61d-540c-4309-8566-71b4c2ece118', 'fc91e064-c083-418e-8928-69bf49db9dc8', 'IMAGE', 'https://cdn.chotot.com/OweKktm8P2RQhRFYik2kcUDoS4WtlKrxkJ5J-VBsqTA/preset:view/plain/ea8cbc364afc344f79f933073611b91e-2996125120359005709.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('51f46efa-3bda-45f5-aaaf-823d60a9b513', 'fc91e064-c083-418e-8928-69bf49db9dc8', 'IMAGE', 'https://cdn.chotot.com/2yWZRVzYkqStbcL0QZGcM-J0iEWs78XCpJvYf5cUSZU/preset:view/plain/c1f1485d30036a85513006d8ae1b859a-2996125120350432183.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('30b2c733-4a0a-4349-b2d1-94ad99884847', 'fc91e064-c083-418e-8928-69bf49db9dc8', 'IMAGE', 'https://cdn.chotot.com/Q0QrXMfoGePc1HzzsK2L6vikAuJzPhxS6Dd3cxb_bMk/preset:view/plain/98523cb283baae449d9bdba9aef32570-2996125120383213349.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('936e9576-14d7-42b2-b9cf-d1b418adefa2', 'P_128466242', 'APARTMENT', 'Ctl 3 phòng ngủ dt87m2 giá 4 tỷ', 'ctl cần bán 3 phòng ngủ , 2 vệ sinh
dt85m2 giá bán 4 tỷ
vui lòng liên hệ!
#ctltower
#chungtranglinh
#canhoduongthigiang', 'UNDER_OFFER', 'Quận 12, Tp Hồ Chí Minh', 87, 4000000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a97c3b11-9d51-4afc-9304-287bfd3f84c2', '936e9576-14d7-42b2-b9cf-d1b418adefa2', 'IMAGE', 'https://cdn.chotot.com/15ebdC9CYu5qQjpNDhXpjdk2WmVu37QmPicLuUsxHko/preset:view/plain/6fc4660bf89ae948fcb51359f2164959-2953946941895747656.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fcdb79c8-3802-48eb-b922-f44fd0897372', '936e9576-14d7-42b2-b9cf-d1b418adefa2', 'IMAGE', 'https://cdn.chotot.com/1nje8w-U1JzBubAVxJiTRKAWNJer3XZftlFBoxjwmhQ/preset:view/plain/01dec8671a4411b2fc7243598b7f58c7-2953946941889831217.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1180e057-6d0d-40e5-933f-aa7c6368b60c', '936e9576-14d7-42b2-b9cf-d1b418adefa2', 'IMAGE', 'https://cdn.chotot.com/uOUy_X3wJjy0m51oupyS_rkseamGjz6x1SFoiYNglW4/preset:view/plain/f38c4f818cdafd8bb0f2968d7032de00-2953946941794794228.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4274a9ae-903e-49b2-8da6-facfc4d4f263', '936e9576-14d7-42b2-b9cf-d1b418adefa2', 'IMAGE', 'https://cdn.chotot.com/y8TYUIblwbCxdUCpi-NILP7VdF1ntcRQyPP74MrHgBc/preset:view/plain/2e091f46546bfcb69defd0242601ae59-2953946941856663634.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bf096073-d88f-4e2b-b639-d7238eb77498', '936e9576-14d7-42b2-b9cf-d1b418adefa2', 'IMAGE', 'https://cdn.chotot.com/IoORURJRH5iVaeQ5kdf-32pOoNh8Xt11SbLKJI0oHGw/preset:view/plain/052521be9f2d6ac5f1713c023257daaf-2953946941803396124.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('40edbb3a-94dd-4da1-bd44-791503e48055', '936e9576-14d7-42b2-b9cf-d1b418adefa2', 'IMAGE', 'https://cdn.chotot.com/uvRQvBDHP8sV3ndhId1DR27FzSu4cGAIElUoODxl7Fw/preset:view/plain/3afa581d4b067162552a06a5121339bb-2953946942146278490.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('28c1ad32-8604-4354-843a-7912879bebc4', '936e9576-14d7-42b2-b9cf-d1b418adefa2', 'IMAGE', 'https://cdn.chotot.com/bU74c2MXm9dfwaA6BIUIC-L4ND4AQlTBNtLF7TT9kwo/preset:view/plain/c7ea06728ff1fa56f5114e796cd1c12b-2953946941747582267.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6af9ffc0-b1d1-4680-82ae-0292f1c0c287', '936e9576-14d7-42b2-b9cf-d1b418adefa2', 'IMAGE', 'https://cdn.chotot.com/DHBDdgd6KB6zL6I-KlMYT2moGVWVU0amQrgN1iVjrFI/preset:view/plain/f351b060f954d925342c9979f4ab3d04-2953946941944421226.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1ca10728-01ac-4735-b4a9-aa438e4b2362', '936e9576-14d7-42b2-b9cf-d1b418adefa2', 'IMAGE', 'https://cdn.chotot.com/x0rHIXeauc19eQVgXgTPvCDM3hKpMc1a98nznFpiqQc/preset:view/plain/79ca4e96ab4bf6c72d48fb2453ccf0b4-2953946941834904801.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('ddec13ed-e0ac-434a-b423-b9eeba3e50c4', 'P_133404857', 'APARTMENT', '🌟 CHO THUÊ CĂN HỘ GIAI VIỆT – Q8. 115m2 2pn 2wc giá 13tr 🌟.', '
🌟 CHO THUÊ CĂN HỘ GIAI VIỆT – Q8. 115m2 2pn 2wc giá 13tr 🌟. 
Căn hộ rộng rãi – vào ở ngay!
🏡 Diện tích: 115m²
🛏 Kết cấu: 2 phòng ngủ – 2 vệ sinh, logia rộng rãi
🛋 Nội thất: nhà đầy đủ nội thất
🌆 Không gian: Thoáng mát, sạch đẹp, an ninh 24/7, tiện ích đầy đủ
💰 Giá thuê: 13tr/ tháng

🛋 Nội thất: đầy đủ nội thất. Giá thuê 13tr


📍 Vị trí: Chung cư Giai Việt – Quận 8, thuận tiện di chuyển sang Quận 5 – Quận 1 – Quận 7
📞 Liên hệ xem nhà: ***- ***
', 'UNDER_OFFER', 'Quận 8, Tp Hồ Chí Minh', 115, 13000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1e0f88ce-469f-4212-ad4e-f6c14f9f5d25', 'ddec13ed-e0ac-434a-b423-b9eeba3e50c4', 'IMAGE', 'https://cdn.chotot.com/wvBh4hOdV4xqkdOz3_FOJTaRHRKIeklR22kNW0omEnw/preset:view/plain/cb7a3ed5f128d8f7186197dcc879959c-2992042586318625882.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('13ec5ad0-00e2-4853-96ef-a58a10a84b26', 'ddec13ed-e0ac-434a-b423-b9eeba3e50c4', 'IMAGE', 'https://cdn.chotot.com/fC_yHbhtKeyvw8kTnuTs0UeDZveXIfUFypPUTSpPCbw/preset:view/plain/77b9926471fd8dae9563f2e80840ed14-2992935267421012023.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('959f2fa7-2a71-4d2b-8981-7d88b5016906', 'ddec13ed-e0ac-434a-b423-b9eeba3e50c4', 'IMAGE', 'https://cdn.chotot.com/G7ggKLrw0alwzihmyyZptnTYFsY5r_CLhrVL1ZpMy3M/preset:view/plain/692f85cc5cf38f826c3276b5ad5ac84c-2992935414600103437.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('911165b9-616b-4642-bded-b58e0f86cc63', 'ddec13ed-e0ac-434a-b423-b9eeba3e50c4', 'IMAGE', 'https://cdn.chotot.com/ufDh7RqnSsvyKBfIxxvW_LQ9LyMqEFFldGV3yWReX-8/preset:view/plain/4e3e7ac3286428c66c9e3545c5a8e87b-2992935433911137805.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7f3cc15a-9940-45b2-9c15-1426d6818b48', 'ddec13ed-e0ac-434a-b423-b9eeba3e50c4', 'IMAGE', 'https://cdn.chotot.com/5X1Ys0XH_3TZdNgSUlxR7AQj-KFsRSG6Y2jUBQyWcDA/preset:view/plain/888783f8c8e48bb77c8d73ce6c011439-2992935470016493069.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2ac464f1-0912-4e36-a600-d0adf144546f', 'ddec13ed-e0ac-434a-b423-b9eeba3e50c4', 'IMAGE', 'https://cdn.chotot.com/jnczSX6O189VuMT2frsgsazgy9uY8ysIwNufsb2bOnw/preset:view/plain/77f0cf2bc1c0473798abe1d84feebbf1-2992935482314454541.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('0a537119-4abf-4f9b-b4ab-10e828df31da', 'P_133142145', 'APARTMENT', '✅Cho Thuê Căn Hộ_1PN 45m2__Thang Máy Hầm Xe_Nguyễn Văn Đậu B.Thạnh✅', 'Hệ thống hơn 1000+ căn hộ khắp các quận chỉ chờ khách iu tới chốt.

✅Hà Dương luxury apartment✅
( Nhiệt tình, Uy tín, Trách nhiệm)
~~~~ ~~~~ ~~~~

✅VỊ TRÍ CĂN HỘ:  Đường số Nguyễn Văn Đậu, Bình Thạnh
- Cam kết hình thật + Giá thật
- Tiền cọc: 1 tháng tiền nhà
✅ Giá Phòng: 9,000,000✅

✅Giá Phòng bao gồm:✅
📢Dịch vụ tốt, chỉ cần xách vali vào ở.
📢Bảo Trì, Sửa chữa, Giờ giấc tự do, Hầm xe rộng rãi.
📢gần nhiều tiện ích, dọn vệ sinh thang máy, hành lang mỗi ngày.
📢Bảo vệ 24/7, an ninh tốt, dân cư yên tĩnh, văn minh. 
📢 Có Thang Máy, ra vào bằng vân tay
📢Full Nội Thất đầy đủ các thiết bị cần thiết….
      ...............
✅Ngoài ra, Dương còn cơ số căn hộ xịn xò khác ở Các Quận:
- Studio, duplex ban công, cửa sổ giá từ: 6tr9
- 1PN Đẹp giá từ: 10tr
- 2PN, Căn hộ cao cấp giá từ: 12tr

📲Inbox Dương hoặc liên hệ hotline / nhắn tin Zalo qua SĐT: em Dương để được tư vấn ngay nhé.', 'UNDER_OFFER', 'Quận Phú Nhuận, Tp Hồ Chí Minh', 40, 9000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b61a5739-c147-480f-9df7-ffea8c9c1cbe', '0a537119-4abf-4f9b-b4ab-10e828df31da', 'IMAGE', 'https://cdn.chotot.com/u4wGb0lUaVhK5nxWzllJ5sZtFGyHv3FCu7JGyqWCews/preset:view/plain/412bd1d6e0452da5358657d45f58b818-2990023850872909721.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dea596d3-bccc-4dbe-9692-8b99478c812a', '0a537119-4abf-4f9b-b4ab-10e828df31da', 'IMAGE', 'https://cdn.chotot.com/8H7HEkrmBxzn8byMvXh60PNn1VBrI4AS0yr_lT0lNfg/preset:view/plain/e6d2c043c4a089b53d7e18c9ae241eb5-2990023856127409531.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('57b11a41-44e3-4d06-ab5c-afbfe3fe2eb8', '0a537119-4abf-4f9b-b4ab-10e828df31da', 'IMAGE', 'https://cdn.chotot.com/ecZWaxR0M8X4vXPGlYOKxcRDNir0xZQLpKsUeK9QmgE/preset:view/plain/301df8a2c9a02ddbec2d129cb4a358ec-2990023856233474673.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d77716e9-e5d8-4fa6-b4d8-b0867e85fdbd', '0a537119-4abf-4f9b-b4ab-10e828df31da', 'IMAGE', 'https://cdn.chotot.com/HANhxwdPztt9kDgxodg6JHXmA8SS56_hKX2BQWIMdCs/preset:view/plain/a0a1052fbaa4768c5b5fcab45bffa890-2990023856292451444.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1e3770a0-c8ee-44c2-bde8-3d9d9b9a1e96', '0a537119-4abf-4f9b-b4ab-10e828df31da', 'IMAGE', 'https://cdn.chotot.com/bQZa_cMpdYFflkjeyHatH0Qh1jSNIvLAGbCoTuSukjg/preset:view/plain/7485f11897749123a0255e84945101c2-2990023856292081561.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b5909721-822a-4d20-84ac-65ee60558e26', '0a537119-4abf-4f9b-b4ab-10e828df31da', 'IMAGE', 'https://cdn.chotot.com/ppxGFjGU27Fy9CwEDKhYSIMQo0GpSyTO4fDi4RFD-2U/preset:view/plain/4561a300b283b4defb31664f5c0f9970-2990023856284985092.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f5a95edd-c88b-44b8-a4f1-70dca3895503', '0a537119-4abf-4f9b-b4ab-10e828df31da', 'IMAGE', 'https://cdn.chotot.com/NGGAicP0ciRkV6VvQr9zhQZes4PqietsIv3TF48qnGI/preset:view/plain/7f64deaabe417695de4299a3ee6661d3-2990023856446629950.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bd4eb562-18c4-4d9b-bd66-49f80455b127', '0a537119-4abf-4f9b-b4ab-10e828df31da', 'IMAGE', 'https://cdn.chotot.com/IBDfWUA2hR59qLdGSUt5xzsOEp20I9F9KyK_S8jAMJU/preset:view/plain/57ccf6321dcf60e56e26c1d2b324ceb4-2990023856271926408.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('54a06feb-f4b6-4b23-a4c6-17ec0f711037', '0a537119-4abf-4f9b-b4ab-10e828df31da', 'IMAGE', 'https://cdn.chotot.com/D1WhFyssOqjq6oQ7waEj8CYtDGQZkdBs0Ry5IgN3T3o/preset:view/plain/4dbb29f7cbe42c9835fe1ee82f7d8c25-2990023856317492709.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ddc8eaf1-bd18-4fad-8c6a-ed89ba38284d', '0a537119-4abf-4f9b-b4ab-10e828df31da', 'IMAGE', 'https://cdn.chotot.com/fM8tGTOa2oPmxvZNVQpEy8nY-GlTJd9nSpPpHP_gvJo/preset:view/plain/2f250b20fbc60863cef750851706b331-2990023856398421165.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('6928ed3e-badf-4599-9fab-9cc82a0a63bb', 'P_133941326', 'APARTMENT', 'Chung cư mini | Full Nội Thất | Có Ban Công Ngay Đầm Sen Mới 100% 🔥', 'Dự án: 
Thông tin chi tiết: Cho Thuê Chung Cư mini | Full Nội Thất | Ban Công 🔥
Dạng Studio - 1PN - 2PN 



🚦 Vị trí : Ngay Âu Cơ - Khuông Việt Tân Phú 


Vị trí thuận lợi : Âu Cơ Luỹ Bán Bích , Quận 10 Quận 11 Khu Công Nghiệp Tân Bình Eon Tân Phú 

Toà nhà có thang máy ✨


Nội thất cao cấp mới keng ✨



Hệ thống PCCC đạt chuẩn ✨



Thang thoát hiểm camera 24/7 cực kì an ninh ✨



🔥 Hỗ trợ deal giá và giữ phòng 🔥



☎️ Liên hệ ( mess / zalo / fb ) : *** Thời Nguyễnn để đc tư vấn xem phòng free nha', 'AVAILABLE', 'Quận Tân Phú, Tp Hồ Chí Minh', 35, 5500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6e8e4e07-5a38-435f-b59a-22552b89ff3f', '6928ed3e-badf-4599-9fab-9cc82a0a63bb', 'IMAGE', 'https://cdn.chotot.com/0E8hG_WSF-AQ8Bim7m9Lej051HllLAodJ4TswGp3xgw/preset:view/plain/db43b11bedfb41b6269ecd795c45629c-2996124816295243594.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1b4f692f-374e-4ce7-a3ee-60fec2a9edec', '6928ed3e-badf-4599-9fab-9cc82a0a63bb', 'IMAGE', 'https://cdn.chotot.com/CEwIDGweaxlzNIrQOlytsuWyZZ6e594fPsZi0Va13mM/preset:view/plain/8864b1e2673c16b4d29de605115c86ad-2996124816606896216.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8695be6d-d008-4c32-b2e3-06791f5b1616', '6928ed3e-badf-4599-9fab-9cc82a0a63bb', 'IMAGE', 'https://cdn.chotot.com/htoytPpKue4DgXYZjwM4zBYoHm4mkrVdJVMQyTCl-Gs/preset:view/plain/41b93744ea5b81637eca6c8d8a8b48ee-2996124817503279374.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('401d873a-76a6-4841-876c-d7b175486ef5', '6928ed3e-badf-4599-9fab-9cc82a0a63bb', 'IMAGE', 'https://cdn.chotot.com/K1MbP5prHvddLDuMfUsKzCWe12wsR7QtdgKAlI2ooVg/preset:view/plain/6ee598275f547300e04fe7e91e1d86e4-2996124816960480934.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('15b6e4d4-f0c0-4aca-80a7-39e5e16ff80b', '6928ed3e-badf-4599-9fab-9cc82a0a63bb', 'IMAGE', 'https://cdn.chotot.com/bwGOsIgVyMVtXEFw80e28NxbzvapL0VnPJdVbuU75Gs/preset:view/plain/b704928cf9a504c46d7b45b59fa5aa0c-2996124817117064119.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7be999e1-0621-4e6e-be7a-c73922433c7b', '6928ed3e-badf-4599-9fab-9cc82a0a63bb', 'IMAGE', 'https://cdn.chotot.com/-ID5u5O5wR1dMo3jHrU6do72lfmmE_Vd5uYYhDSTLK8/preset:view/plain/a1b6a29ac4b314039f185162ba61aeda-2996124816765038158.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e886f2cd-3e41-4ac9-bf53-5cb3f865cb91', '6928ed3e-badf-4599-9fab-9cc82a0a63bb', 'IMAGE', 'https://cdn.chotot.com/ywQFZpQloChHIlvHJH8VgpBO0QFLUY7_C5acB_0CU9g/preset:view/plain/9d17452d018e8ce2b0cc694a36b5e60a-2996124816798559003.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fb8e0700-c761-4e50-a4d5-bf5ce46f3eca', '6928ed3e-badf-4599-9fab-9cc82a0a63bb', 'IMAGE', 'https://cdn.chotot.com/pO-L6ZFBeO3hloHoBqc0KNgZFQNQ5wEWM8Ge00wKiF4/preset:view/plain/1b9bd3572e23d3457e6434f1f586c63c-2996124817035627573.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1cd2b672-58fa-4d38-a49d-273cec044b5a', '6928ed3e-badf-4599-9fab-9cc82a0a63bb', 'IMAGE', 'https://cdn.chotot.com/RmMR_eaIG8eLa9sPmqEu3mczPC_5EViHKiSYSEGOcbk/preset:view/plain/d55f241dc7cd00cfecc9028871ac3439-2996124816865628110.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1cf77e02-3fb0-4d45-8c03-9e5629168c4b', '6928ed3e-badf-4599-9fab-9cc82a0a63bb', 'IMAGE', 'https://cdn.chotot.com/2Yldthq0p1TnL-R6gSf_0aNv3D3olWLy_UoRQ34ad1Y/preset:view/plain/7b121e9f3c44c889f972c4d605165069-2996124817515320616.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3aaf9bed-2825-4439-8154-dd1fdbc32ecf', '6928ed3e-badf-4599-9fab-9cc82a0a63bb', 'IMAGE', 'https://cdn.chotot.com/f16cR9LXX62jQqqB3pZO7rXloP-5Ie4fuxQZD-8hdNI/preset:view/plain/ffe626820936c9c6f2f48c05e2d8a750-2996124817285099909.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('19b038ea-8c23-4304-9bbb-f7a4f677b0e2', 'P_130589864', 'APARTMENT', 'Chuyên Cho thuê giá tốt căn hộ Vinhomes Central Park ', '- Cần cho thuê gấp căn 3PN 116m², view sông mát mẻ cả ngày, 2 ban công view cực chill.
- Giá chỉ 35tr/tháng, full nội thất mới và sạch sẽ, chỉ cần xách vali tới ở.
- Chủ nhà dễ thương.
- Nhà đang trống in liền đc, xem nhà 24/7.

P/S: Ngoài ra, Chúng tôi còn nhiều căn hộ khác cho thuê ngắn hạn, dài hạn giá tốt khác tại Vinhomes Central Park.

Căn hộ 1PN giá chỉ từ 17tr/tháng. Căn hộ 2PN giá chỉ từ 20tr/táng. 3PN giá chỉ từ 30tr/tháng.
Giá thuê theo ngày chỉ từ 1tr/phòng.

+ Check in ngày - tháng - năm.
Liên hệ ngay Huyền *** - (Viber, zalo) công ty Ruby homes SG để chọn nhà đẹp, giá tốt nhé.
* Tiện ích:
- Căn hộ trang bị đầy đủ nội thất, giống như homestay, có máy giặt, tủ lạnh, có bếp nấu, chén bát, lò vi sóng. Nhà tăm có đầy đủ kem đánh răng, bàn chải, sữa tắm gội. Chỉ cần xách vali tới ở.
- Có phòng gym, hồ bơi, khu BBQ, khu vui chơi thể thao ngoài trời cho cả người lớn và trẻ em, công viên rộng lớn 17 ha... (free). Khu ẩm thực phong phú, khu mua sắm bậc nhất Sài Thành.
* Hãy thử trải nghiệm cuộc sống sang chảnh, tiện nghi tại Vinhomes Central Park với giá siêu ưu đãi.

* Lý do chọn chúng tôi: Tận tình - trách nhiệm - nhà sạch đẹp - giá tốt.', 'UNDER_OFFER', 'Quận Bình Thạnh, Tp Hồ Chí Minh', 118, 35000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6544b586-e00c-4aaa-95a4-d0b2152e7c89', '19b038ea-8c23-4304-9bbb-f7a4f677b0e2', 'IMAGE', 'https://cdn.chotot.com/9CV8yxI6N854b_39kvWpNtpvyIo6l_0z2iuylWuK_ko/preset:view/plain/4c11dcf33788fd16165eaba3a9c70727-2969312762788001129.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2e87e0c0-7646-408d-b84f-f9f73eba3074', '19b038ea-8c23-4304-9bbb-f7a4f677b0e2', 'IMAGE', 'https://cdn.chotot.com/GmPPHkzF3nwX2XkKQ_yoSew_44ktdTCwk0PTmQgMKIo/preset:view/plain/c4de07fb1f7ed23b02d138ea8182409c-2969312848953205066.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('23c4b9fc-0525-430f-815d-e6716af2694b', '19b038ea-8c23-4304-9bbb-f7a4f677b0e2', 'IMAGE', 'https://cdn.chotot.com/-1Z5TkhAklE4KWCQQjrHcf2z_rn37l0ehX_4a13bvYE/preset:view/plain/974c81f3850baaa3920c18705835c744-2969312848652581033.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c4fc1b78-fd77-462d-982d-f0aaf7367017', '19b038ea-8c23-4304-9bbb-f7a4f677b0e2', 'IMAGE', 'https://cdn.chotot.com/ws78QaqGqMKsqJtNKYw5nFkg3YK2jqG-mtREFZDU01I/preset:view/plain/a3fcd6f81d6e2bea5bd4fa9ed6ffa678-2969312848724194679.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dde505af-5784-4119-9e52-8f3d1e205e56', '19b038ea-8c23-4304-9bbb-f7a4f677b0e2', 'IMAGE', 'https://cdn.chotot.com/lO5f3u5qRICe4bwfSwrD4tvBMDYcksDZaN-SQml4tcI/preset:view/plain/de57a71e36f64b4d9b010347e830deae-2969312848690237190.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4f132423-5691-424b-8e98-241e8299576f', '19b038ea-8c23-4304-9bbb-f7a4f677b0e2', 'IMAGE', 'https://cdn.chotot.com/ZXuFXM-FRE_LmUKFZNeG1H0dKcwANhYB4N2Qz8O6JkI/preset:view/plain/b8db80618316209d00aab23ce4e0b714-2969312849961976941.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f23717f3-04af-4fb1-b011-c4ad2a09ae1e', '19b038ea-8c23-4304-9bbb-f7a4f677b0e2', 'IMAGE', 'https://cdn.chotot.com/I24sBeIdAT1JREEPKc4biypE5dnUFsvDkPCA-jdhMrM/preset:view/plain/5612617c99de99f153561dfcc1ffc8ce-2969312849005473479.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('aa26d37e-1464-4ae7-81f9-307af2c3b443', '19b038ea-8c23-4304-9bbb-f7a4f677b0e2', 'IMAGE', 'https://cdn.chotot.com/VKkYUpgCoUS3Dkxfat_JxgHlDvzlcHMrwdEQI90WGZ4/preset:view/plain/1016982895a8519513b8f7c489dfc048-2969312945727060137.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ee4af32b-30d3-4e3d-96fc-48582c39099d', '19b038ea-8c23-4304-9bbb-f7a4f677b0e2', 'IMAGE', 'https://cdn.chotot.com/RjyVlnlSf2xHCpa4M_asEqEmoZ7qMiqE--b4CUBV-No/preset:view/plain/5a6fe8ce038f0173af003e4672041381-2969312965847437062.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8e5b8261-8da3-4eba-ae42-4f2230e917be', '19b038ea-8c23-4304-9bbb-f7a4f677b0e2', 'IMAGE', 'https://cdn.chotot.com/TRD35Efo9Jz2igta0dVAVzI4QJJV6-ktJLxzAI9tlpI/preset:view/plain/87a1862bf11d681c059c0bbf6939edc3-2969313013663420166.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1ddee35c-cf18-4da5-a666-7c87a1b93978', '19b038ea-8c23-4304-9bbb-f7a4f677b0e2', 'IMAGE', 'https://cdn.chotot.com/valxZlzDvZ5q3_EXqoNQ0gQR34I5DOQWQu5_AQMaJSA/preset:view/plain/2be01d0ed6b951730c64e6a403fbe514-2969313052855586566.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5a1b1d4d-1fd0-4e41-967c-09946cd245ef', '19b038ea-8c23-4304-9bbb-f7a4f677b0e2', 'IMAGE', 'https://cdn.chotot.com/_xJqTi9ICdTVDf1wyAX_yfCwUwxvYplm8JyvWYWlnAM/preset:view/plain/0087f5ab1212628ac9e5f765997bf1d3-2969313076792768681.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('0a107bee-d1f8-4943-8f7b-df734575a32f', 'P_132418109', 'APARTMENT', 'Studio Full Nội Thất ngay Lotte mart Quận 7', 'Dự án: 
Thông tin chi tiết: 🔰 STUDIO SIÊU THOÁNG RỘNG CÓ BAN CÔNG Ở LỚN SÁT LOTTE Q7 - CẦU KÊNH TẺ

🎉 PHÒNG MỚI NỘI THẤT MỚI 100%🎉

🌷Thuận tiện qua các quận trung tâm Q1,Q4,Q5,Q8,…

🌷 Ra vào vân tay giờ giấc tự do

🌷Có thang máy

🌷Phòng mới, nội thất mới', 'SOLD', 'Quận 7, Tp Hồ Chí Minh', 25, 5000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fec5c9ee-2d18-43ad-b84c-f1ee049f6659', '0a107bee-d1f8-4943-8f7b-df734575a32f', 'IMAGE', 'https://cdn.chotot.com/LWXvO3njxtz8lZztFu5V7S_N3o3krPzCJ-NeMjIipZ0/preset:view/plain/a1565027ce1ae47b5cb0b82c7756debb-2984508851020052349.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f83a3b91-0e9d-4cef-942e-be7cadf99343', '0a107bee-d1f8-4943-8f7b-df734575a32f', 'IMAGE', 'https://cdn.chotot.com/p5Cf8OdTinwZZyyBHN8-uY78h_0kdj6hUbGj9x8rfds/preset:view/plain/5f69fe098d5ac00e3cbd15391f9246a6-2984508851042710737.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ede74e39-97b4-4b86-a702-1813521144d4', '0a107bee-d1f8-4943-8f7b-df734575a32f', 'IMAGE', 'https://cdn.chotot.com/qhGk7wgVsCqMYST1RrMaCM0CyOvmZFMsLQxwz3PUcIo/preset:view/plain/5f3edb389ab04976939f555476eef017-2984508851198291327.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('11dc1667-3485-4524-81b0-114771936be2', '0a107bee-d1f8-4943-8f7b-df734575a32f', 'IMAGE', 'https://cdn.chotot.com/4Wl3TbPb-igVEFr5lOnVzazIq6QtKMzwJXSlO9A5ot0/preset:view/plain/41166b68bb3312870c84af40f47c89fa-2984508851177278027.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0682d440-3686-4aa2-9c36-a30e2107f2cb', '0a107bee-d1f8-4943-8f7b-df734575a32f', 'IMAGE', 'https://cdn.chotot.com/NKT_l2ZI8Hh7OobWIOZZsSTyG0ql3fPRunvkbBSrrg8/preset:view/plain/3fe7f2116290d8d5f00c6b4f787c351c-2984508851415017116.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b368e403-93bd-483f-a116-9cc59f8ea744', '0a107bee-d1f8-4943-8f7b-df734575a32f', 'IMAGE', 'https://cdn.chotot.com/EVzm16F2amNJeCxcrnh584yiV0elGBjHZJdAvS7si5A/preset:view/plain/f313b39955fd71c8cea6cc0711eed8ea-2984508851465848110.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6a07202d-7c4a-42e0-98e1-395a971e1f6b', '0a107bee-d1f8-4943-8f7b-df734575a32f', 'IMAGE', 'https://cdn.chotot.com/Bv46MNRldp5Rv8t_tVhLxREP-X55nGB_T9VhO4hu6dg/preset:view/plain/84f59897d81badb2e94b234ed88349b1-2984508851374283969.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('182a4c97-562e-4fa1-9664-8ccf0bebbed3', '0a107bee-d1f8-4943-8f7b-df734575a32f', 'IMAGE', 'https://cdn.chotot.com/L1R0Bm-LYIH1IFIIRNct_ZdOfsjpJwyToYluETgIkVc/preset:view/plain/c0c44231106a77e1fb72350c22b9a4df-2984508851281711829.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d6e13de8-2b5d-4c5c-8771-ac9cd84a81b7', '0a107bee-d1f8-4943-8f7b-df734575a32f', 'IMAGE', 'https://cdn.chotot.com/ZUcABG17oJCMvW77zawH1YoeQqbK9x6qxAihhzcNqqM/preset:view/plain/f4650e2784ec6abbba91a9dc1272f9f7-2984508851307814818.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f8be77b6-689d-4318-92fe-3a95c2f3df67', '0a107bee-d1f8-4943-8f7b-df734575a32f', 'IMAGE', 'https://cdn.chotot.com/TyZ0krUPkaAodogKCQUU-aDbLSSqhZ_WYvpOk6cFgw8/preset:view/plain/fcc38ad4f305e04573f33f56887f0ae0-2984508851288730450.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e0c5e45c-a31b-4fae-b152-743d1eef45ad', '0a107bee-d1f8-4943-8f7b-df734575a32f', 'IMAGE', 'https://cdn.chotot.com/w6hVAL1OYsYFqgPTu6jcoRLGytvIbT0LwCSrtHsp4Bg/preset:view/plain/7d51e17bbdd5cbaf396825ce7bf6bc60-2984508851286146752.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8b3b5147-7710-4009-8dba-49984d1aec29', '0a107bee-d1f8-4943-8f7b-df734575a32f', 'IMAGE', 'https://cdn.chotot.com/gofXcCOEEfSAjQATxNxcTPfGdKTS8ZTEKF67eskureQ/preset:view/plain/7062fc961c49eb777baa28a1d87f5098-2984508851376264105.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('895fcacb-9a26-4930-9639-4ec0b54bc838', 'P_133031130', 'APARTMENT', 'Cho thuê căn hộ 2PN 2WC Jamila Khang Điền, full NT, 11tr/tháng', 'Jamila Khang Điền, Song Hành, Phú Hữu, TpHCM.
Cần cho thuê căn hộ 2PN 2WC.
Nhà full nội thất.
Giá thuê: 12tr/tháng.
Liên hệ Ms Liên để biết thêm thông tin chi tiết và xem nhà thực tế ở Jamila.', 'AVAILABLE', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 76, 12000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1d6f8225-22a7-4e6e-b182-d5c663085b5a', '895fcacb-9a26-4930-9639-4ec0b54bc838', 'IMAGE', 'https://cdn.chotot.com/o3LipiqKydEBXSNlew1CueBGiFdEcz5KsjXm_hl81LY/preset:view/plain/7eee7b6b22a4bd5dccdd14c2193dcc20-2989433738318017506.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8cdd7738-91c8-471a-9def-d6b2d8436c70', '895fcacb-9a26-4930-9639-4ec0b54bc838', 'IMAGE', 'https://cdn.chotot.com/DB_pTSyvMbEcTKE9oz3PSNN_Ao9xNyypHUSEYwWfIZ8/preset:view/plain/026f2b215b584da6f13002108afa64b7-2989433738187477078.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0c3d531a-5eac-48bd-938b-f5a818e5c74b', '895fcacb-9a26-4930-9639-4ec0b54bc838', 'IMAGE', 'https://cdn.chotot.com/IsqnPXwPV4SnIeS5HgLGHTJ5_bd63-KepMZRoX5exvg/preset:view/plain/c7a35299a36b09804710a4cb39ff3fe4-2989433738212171378.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bddb05bd-9914-4e38-bf0c-fd51cc03d452', '895fcacb-9a26-4930-9639-4ec0b54bc838', 'IMAGE', 'https://cdn.chotot.com/_7tEiEL9BUvj01dkKg2T4L4nmLRQHRSKjmWziuWbj2c/preset:view/plain/828fea7ccc2b4c1748f73c29b3a8b2a0-2989433737898783321.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6a0c4e12-c1f2-4e38-907f-dd121850c6a3', '895fcacb-9a26-4930-9639-4ec0b54bc838', 'IMAGE', 'https://cdn.chotot.com/z-jQIS3GbnyGjoPDmQgb44otsqmBgiG4Az_0iwu6isg/preset:view/plain/71442147cb0158dd1d7efa726b796bbd-2989433738117343857.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4a64de62-7361-4074-8da9-a40a0c6667de', '895fcacb-9a26-4930-9639-4ec0b54bc838', 'IMAGE', 'https://cdn.chotot.com/lMQazeqkaZEniGVZKmWXfPA4U5f2b35V8Qf-09XtCVw/preset:view/plain/e893ece780b78966ba2b250ce438a1ed-2989433738346831005.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('2385f2bc-dbb0-46b1-8874-f6fa60b05870', 'P_133871181', 'APARTMENT', '❌ 2 PHÒNG NGỦ - NGAY ĐẠI HỌC KINH TẾ, BÁCH KHOA, Y DƯỢC,..', 'Dự án: 
Thông tin chi tiết: ✅ Giờ giấc tự do - PCCC đầy đủ
✅ Full nội thất: máy lạnh, giường - nệm, kệ bếp  ,tủ quần áo , rèm cửa , bàn , máy nóng lạnh, gương .
Cho nôi mèo

☎️☎️ Liên hệ Zalo/Call: *** (Tâm) để được tư vấn và xem phòng miễn phí nha', 'UNDER_OFFER', 'Quận 10, Tp Hồ Chí Minh', 45, 6800000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('50868117-e001-408c-ba68-c6610f583668', '2385f2bc-dbb0-46b1-8874-f6fa60b05870', 'IMAGE', 'https://cdn.chotot.com/3hy0m6Rl8h6Ewdxfm5zFo4T4Xx39GeMePwuE8Dt9yE4/preset:view/plain/77c6cb589925823c4fe94fabd9242aeb-2995558512762898809.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0475b79c-0172-43df-9ae9-6594e3883478', '2385f2bc-dbb0-46b1-8874-f6fa60b05870', 'IMAGE', 'https://cdn.chotot.com/LOQOprFrDYpOYSgZkF8Cj0auTwZ4FxepSl42T0Rnh6E/preset:view/plain/9f1821a79cbc48835b1932ac6b527493-2995558514026608015.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d8ebfb21-057c-43a3-89c8-a668959191d1', '2385f2bc-dbb0-46b1-8874-f6fa60b05870', 'IMAGE', 'https://cdn.chotot.com/g4V4qpTw_iYKVhHPUv0W8ztG1a_rAGXMgklSqyD0E9c/preset:view/plain/772e00e60fc7644ac66c28a3bb1b7fbc-2995558514725567564.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('26b3fdb9-df66-43f9-a381-d357a7167a87', '2385f2bc-dbb0-46b1-8874-f6fa60b05870', 'IMAGE', 'https://cdn.chotot.com/6JFmVdL4kJcUgd6wzBXD9NFSvtzwBydwAJT5yrir5U0/preset:view/plain/8f4551f4a4157b6965cf774405c745a8-2995558515939395044.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8220a435-f7bc-463c-bee2-a06ebf24b492', '2385f2bc-dbb0-46b1-8874-f6fa60b05870', 'IMAGE', 'https://cdn.chotot.com/qaslo4ySTHRDWK5JtwurmoXhrOLuY6N65SQucyd_rxY/preset:view/plain/12fa0e58ddf868babee0441141f85612-2995558515933923705.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('137db29d-1894-467b-b41f-ff5aa3f132c0', '2385f2bc-dbb0-46b1-8874-f6fa60b05870', 'IMAGE', 'https://cdn.chotot.com/KYQMw2mVmAvPnhudE3DtugAi0H3llT9JNP78XiPpZC0/preset:view/plain/d7598b02ae195cf76e25873991df8148-2995558515888944527.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('dba63ea6-f7d0-4733-beb9-9d0533fd750a', 'P_131236964', 'APARTMENT', 'Cần bán chung cư 85m2 (3pn) - giá 3,580 tỷ - sổ hồng sang tên liền', 'Chung cư Westgate An Gia.
Căn 3pn2wc (85m²).
Giá: 3,580 tỷ sổ hồng riêng.
Ngân hàng hỗ trợ vay đến 80%.
Nội thất:
+ Giường, tủ quần áo.
+ Tủ giày.
+ Tủ bếp trên dưới.
+ Bếp từ, máy hút mùi.
+ Rèm và giàn phơi.
Liên hệ: *** ( Trung Trực )', 'AVAILABLE', 'Huyện Bình Chánh, Tp Hồ Chí Minh', 85, 3580000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('291c2c2d-706f-46f2-925b-539f7e491a36', 'dba63ea6-f7d0-4733-beb9-9d0533fd750a', 'IMAGE', 'https://cdn.chotot.com/QFmOEvyQcA4z2FwIFJBsjkMATe9snQ63vji-habTxg4/preset:view/plain/a3e6cfa5833f61db916b0d04b5513c98-2984701551109440766.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('150101ed-bc88-41aa-a643-a317ebf70946', 'dba63ea6-f7d0-4733-beb9-9d0533fd750a', 'IMAGE', 'https://cdn.chotot.com/q9loerlJdpK-P-H4JbqyOJtOYSvt9RGFyrY38rvyvB4/preset:view/plain/aceb26e7c3f0249f695b710b9f1408b3-2984701551167066837.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e7542274-084b-42cb-9dcf-baf51ceee803', 'dba63ea6-f7d0-4733-beb9-9d0533fd750a', 'IMAGE', 'https://cdn.chotot.com/zFGAiVrNYVVGYm5uqKC1MrRTWr0Rk3YwJcfS7c6G_CI/preset:view/plain/591075c499dca4758aac78808d839b28-2984701551109152126.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2602c32d-08ef-4f5c-a2c5-736c0ded2402', 'dba63ea6-f7d0-4733-beb9-9d0533fd750a', 'IMAGE', 'https://cdn.chotot.com/IeyZu8R5731awGukfbzTNa7BUBORCYd7UWGIbhvXiRc/preset:view/plain/480247b77ac2d7b8b1b7e3bd7d216313-2984701551243036948.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('23ab4a4b-2a27-4f7d-a021-5aea666b5414', 'dba63ea6-f7d0-4733-beb9-9d0533fd750a', 'IMAGE', 'https://cdn.chotot.com/hZftZS6xZ6WPYUJLAfl7CQk0rLKIhgr1A2C5ozlms2w/preset:view/plain/a14ab50cfe27459519adb407141eef63-2984701551248441212.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4dccb01b-36ae-4c28-b298-06fe2d8f3dd9', 'dba63ea6-f7d0-4733-beb9-9d0533fd750a', 'IMAGE', 'https://cdn.chotot.com/9T3UYwks9HIR7xgrz0Dw7ml4wLpk9DGoy-MsrySoQBU/preset:view/plain/d0c05c72041268b57fe8b03a61c392ac-2984701551263361125.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e8a7b3a4-5585-4ced-bd19-7c4176286893', 'dba63ea6-f7d0-4733-beb9-9d0533fd750a', 'IMAGE', 'https://cdn.chotot.com/0QQ7Yio5NYnm9PpbmgvSYzzzmEzlR5nh5TjevoxOdqk/preset:view/plain/052d4bba333d864d47417c82eaf74760-2984701551065563661.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('bf6fc466-093d-4375-b094-6b68861f2d91', 'P_133640853', 'APARTMENT', '🔥CĂN HỘ 2PN BAN CÔNG FULL NT-NHÀ MỚI🔥QUẬN 10-Q3-TÂN BÌNH-BẮC HẢI-Q11', 'Dự án: 
Thông tin chi tiết: 🔥NHÀ MỚI - FULL NT - GẦN Q10-Q3- TÂN BÌNH- SÂN BAY-PHÚ NHUẬN-NHÀ GA T3-BẢY HIỀN-HOÀNG HOA THÁM-HOÀNG VĂN THỤ...

Giá thuê từ 7.300.000đ/tháng (tùy vị trí và tầng).
Phòng mới xây 100%, sạch sẽ, thiết kế hiện đại.
Không gác, không gian vuông vức, dễ bố trí nội thất.
Có trang bị full nội thất theo nhu cầu của khách thuê.
Phù hợp ở nhóm bạn hoặc gia đình.
Tiện ích tòa nhà
Hệ thống an ninh với camera giám sát.
Ra vào an toàn, khu dân cư yên tĩnh, văn minh.
Khu vực luôn sạch sẽ, được quản lý và vệ sinh thường xuyên.
Chỗ để xe thuận tiện.
Vị trí thuận tiện
Từ phòng có thể dễ dàng di chuyển đến các tuyến đường lớn như Bắc Hải, Thành Thái, 3/2, CMT8, Hoàng Hoa Thám, Cộng Hòa, Út Tịch, Trường Chinh, Nguyễn Thái Bình, Phạm Văn Hai, Lê Văn Sỹ và Âu Cơ. Chỉ mất khoảng 10 phút để đến Sân bay Tân Sơn Nhất, giúp việc đi lại và làm việc trở nên thuận tiện hơn.
Tiện ích xung quanh
Chỉ trong vài phút là đến chợ, siêu thị, cửa hàng tiện lợi, ngân hàng, nhà thuốc, phòng gym, quán cà phê và nhiều quán ăn đa dạng. Gần các tòa nhà văn phòng, khu kinh doanh sầm uất và nhiều trường học, rất thuận tiện cho cả sinh hoạt và làm việc.
Đây là lựa chọn phù hợp cho nhân viên văn phòng, tiếp viên hàng không, kỹ sư, sinh viên hoặc các cặp đôi muốn tìm một không gian sống mới, sạch sẽ, an ninh với mức giá hợp lý ngay trung tâm Quận Tân Bình.
Liên hệ ngay để xem phòng thực tế và chọn vị trí đẹp. Số lượng phòng mới còn hạn chế.', 'SOLD', 'Quận 10, Tp Hồ Chí Minh', 50, 7300000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cbbef56c-36bc-45f0-8d0a-ab27c845a6cc', 'bf6fc466-093d-4375-b094-6b68861f2d91', 'IMAGE', 'https://cdn.chotot.com/P1zmuoPxaysXLUJNS8OopPbw2q5aMICMQtmt-oZnCmk/preset:view/plain/6a4d028ac2bdae7f0cbbaba41c923af4-2993823769276442536.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('59fd6f6b-46e5-488b-aab0-b340db26d003', 'bf6fc466-093d-4375-b094-6b68861f2d91', 'IMAGE', 'https://cdn.chotot.com/e2Pnlz5p3eJQRn_ZQDPenwfGMrOkg6JjH3rz-WUlFT0/preset:view/plain/5bfa82ec97e3c7324587c460f610e1f2-2993823769415243174.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('00f09ede-fe61-48ab-8fe8-5dc1385d6c16', 'bf6fc466-093d-4375-b094-6b68861f2d91', 'IMAGE', 'https://cdn.chotot.com/fHedi3YdlKnfC-j97BscTY1XPyWkhjTxOnUy-KEm4Yk/preset:view/plain/5a524df258471738797ae711c5a7565d-2993823769559909943.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fc181b04-2c58-4131-81ad-7b161534afbc', 'bf6fc466-093d-4375-b094-6b68861f2d91', 'IMAGE', 'https://cdn.chotot.com/8xag44ItEa__mXarqNDaHHBPMWYrDTsvHWj75kAgYXU/preset:view/plain/e168b9b031d3e0829dba80e45e5c49d0-2993823769811533632.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('84e3dbbf-13bc-4df1-910c-bed5bbd542de', 'bf6fc466-093d-4375-b094-6b68861f2d91', 'IMAGE', 'https://cdn.chotot.com/R100EAI_8nrxzn-YXpDmL2cqKqoRQjiQhU-1PBsiGv8/preset:view/plain/cbb54efbab7580883890d31cea6c4d1d-2993823769766372066.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b6394996-0bfa-4505-af38-390f40fc805a', 'bf6fc466-093d-4375-b094-6b68861f2d91', 'IMAGE', 'https://cdn.chotot.com/2LWWYkROIWVc0F9Nz2bwPa8DZlMEg1OTM-4LCkqmw6U/preset:view/plain/1418ec4d229808cfb2dce5192ef13c4f-2993823769549575794.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('10065147-139a-4e2d-9b66-43fd5c042ac4', 'bf6fc466-093d-4375-b094-6b68861f2d91', 'IMAGE', 'https://cdn.chotot.com/CUI2aqc9HCu7zqp_w9NKo9wriA1FpNnnKEu0Dg7SO_A/preset:view/plain/cc1b3e830effba32b923dc7a347152da-2993823769597636606.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('de8bd32c-c134-4866-83b3-87db9a62fb3d', 'bf6fc466-093d-4375-b094-6b68861f2d91', 'IMAGE', 'https://cdn.chotot.com/JBNTdzLRTiKmT3czkZb_o19bRnPB6vLDmVpDnWc3SuM/preset:view/plain/c38f20d3483abe4333c4c6843353fe5f-2993823769582925020.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f69da584-0f86-400c-ac6a-0efc0bcc013c', 'bf6fc466-093d-4375-b094-6b68861f2d91', 'IMAGE', 'https://cdn.chotot.com/dcx904FrKe1RSEgHl9qLX7ZLMJuBaLwArKjju37sweI/preset:view/plain/c2c27a72ae13bf7aae12cf0e44342292-2993823769494570065.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0e4c7ee0-47a8-4e20-a659-e442173434b5', 'bf6fc466-093d-4375-b094-6b68861f2d91', 'IMAGE', 'https://cdn.chotot.com/t59vhqeXJbXRi1jFClsnlhLKtpFDbbeQEZ344HtuKmU/preset:view/plain/8f8a491ea65bfb7293d6be683b799f87-2993823769816076152.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4ddd3e07-7a4d-4c64-aa68-afcb300c77a3', 'bf6fc466-093d-4375-b094-6b68861f2d91', 'IMAGE', 'https://cdn.chotot.com/40mbImgsBbd881RWqGdAeRH4X-aw9AvMxhWufT1do8o/preset:view/plain/bc04d4955f2357a9be9fb9acff86eeae-2993823769614764910.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6b6844b5-b639-41b7-aaf8-5d125ec8f287', 'bf6fc466-093d-4375-b094-6b68861f2d91', 'IMAGE', 'https://cdn.chotot.com/YBfVZAiS_QmrbIpLjlwaQynRFYtTpfbWuvk3cpkoyiA/preset:view/plain/dcd640d705712fc3f5d6d65a443f5c49-2993823769950342851.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('7d7847c7-3f8f-4d39-9e8c-2388dc85a83f', 'P_132343128', 'APARTMENT', 'Căn 2PN View Hồ có nội thất 8,5 triệu/ Cơ bản 7 triệu. LH Hương', 'Dự án: 
Thông tin chi tiết: Anh chị cần thuê căn 2PN ưu tiên chọn view hồ bơi :
- Căn nội thất cơ bản gắn tường. Giá thuê 7 triệu
- Căn full nội thất. Giá thuê 14 triệu

Liên hệ Hương Xem nhà : *** có zalo', 'AVAILABLE', 'Huyện Bình Chánh, Tp Hồ Chí Minh', 59, 7000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d6d8e0b0-3907-454c-8a42-2d61cd18df05', '7d7847c7-3f8f-4d39-9e8c-2388dc85a83f', 'IMAGE', 'https://cdn.chotot.com/mTCvIFiTX7jQAhaqyYKuD5N9mOFLXzrJXXu75wr2_8U/preset:view/plain/31c5bd260f825c361ae08feeba016e42-2983954241195055188.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6126977a-9c5a-470b-8b33-ddf6349ff3a9', '7d7847c7-3f8f-4d39-9e8c-2388dc85a83f', 'IMAGE', 'https://cdn.chotot.com/k5lVXGT_xzCX_NrJR_8hiOA5nI9khncfL-fq-9EVoj0/preset:view/plain/966b28e62f7211c3b71d6c912a2dce14-2983954241217214787.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a99dcdf1-1db6-4401-83a0-03657b270431', '7d7847c7-3f8f-4d39-9e8c-2388dc85a83f', 'IMAGE', 'https://cdn.chotot.com/IlDmL7JJWiV1oIhsnzCFNZBifIcCksVCQ6gWfq4UISo/preset:view/plain/d774add0967c0ce6c83307bf2e2196e6-2983954241228054177.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('954b2898-6460-4196-bbcc-bdf4b157c423', '7d7847c7-3f8f-4d39-9e8c-2388dc85a83f', 'IMAGE', 'https://cdn.chotot.com/AUvbkmviErO4txhGiPK5iIjAfsvJ7SzYAAvOCe5O-Yo/preset:view/plain/102a5194baa353e2bafac1c4b868b0f0-2983954241623753087.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d281dd8b-dc7a-4fff-88e5-42ca33e2d451', '7d7847c7-3f8f-4d39-9e8c-2388dc85a83f', 'IMAGE', 'https://cdn.chotot.com/ji2uFQdr5E36NquQT0uBAWI_W_mu7qrIQj50nQksbko/preset:view/plain/88e7ebffd44d1e78ad5d4b32350f1cf8-2983954241707645528.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4130f4b8-ce68-4c22-926d-e847097e210b', '7d7847c7-3f8f-4d39-9e8c-2388dc85a83f', 'IMAGE', 'https://cdn.chotot.com/cczMXwZCo_MTpIQx0mRRthSRw9OSZQ4m28CJH3RgEkc/preset:view/plain/52c718e5e40ea74aa407c8fb8514af70-2983954241316530710.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('2fc8e9b6-449e-4652-b92c-c582d0f24ad8', 'P_133741374', 'APARTMENT', 'Căn Hộ Duplex Ban Công Full Nội Thất Cao Cấp Tân Hưng, Gần Lotte , Q7', 'Dự án: 
Thông tin chi tiết: SIÊU PHẨM DUPLEX FULL NỘI THẤT CAO CẤP – ĐƯỜNG SỐ 37, TÂN HƯNG, QUẬN 7 

🌟 Điểm nổi bật:
✨ Thiết kế Duplex 2 tầng hiện đại, tối ưu không gian sống.
🛋 Full nội thất cao cấp – chỉ cần xách vali vào ở.
🌿 Không gian thoáng mát, đón ánh sáng tự nhiên.
🍳 Khu bếp tiện nghi, phù hợp cho người thích nấu ăn.
🔐 Tòa nhà an ninh, giờ giấc tự do.

📍 Vị trí vàng: Đường số 37, phường Tân Hưng, Quận 7.
Chỉ vài phút đến:
• Lotte Mart Quận 7
• SC VivoCity
• Đại học Tôn Đức Thắng
• Đại học RMIT
• Đại học Tài chính – Marketing (UFM)
• Khu đô thị Phú Mỹ Hưng
• Thuận tiện di chuyển sang Quận 1, Quận 4 và Quận 8.', 'SOLD', 'Quận 7, Tp Hồ Chí Minh', 40, 6000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5ddbfa32-2cee-494d-a5e3-1a10148a7338', '2fc8e9b6-449e-4652-b92c-c582d0f24ad8', 'IMAGE', 'https://cdn.chotot.com/nBrS8Lrk3CyJvGv4pgX3HO3uTOHGON3Jszi8goHjSgQ/preset:view/plain/f801d0ef879ccbc72e214db8a5efb47b-2994587417780999024.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('41f7f558-6b8a-433a-bcc5-559485c0fb0b', '2fc8e9b6-449e-4652-b92c-c582d0f24ad8', 'IMAGE', 'https://cdn.chotot.com/R5ZJIBN5SDvBdAxu8tMKX9U5PwadBuZHSjzkR6-keDA/preset:view/plain/ae9f0140fbf93bcaef4282375958e429-2994587432410862448.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e86df4f2-3ce8-4f96-bccb-dd5e04ddb2be', '2fc8e9b6-449e-4652-b92c-c582d0f24ad8', 'IMAGE', 'https://cdn.chotot.com/H0414MHQcysQujdroMqkjnpayux5rK8YRDKv13eUnJU/preset:view/plain/79629bcd768eeba18cfb636667e0cc9d-2994587432341858561.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('180e14eb-b290-4a72-9424-26086b8d7a53', '2fc8e9b6-449e-4652-b92c-c582d0f24ad8', 'IMAGE', 'https://cdn.chotot.com/qdei0AePeU1t5fzJEv1eHCHqa_cGGs-S-FrURk4PWbs/preset:view/plain/d37a81bbdc72f8937c52c27f65c498ba-2994587432466825818.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c0eba6f9-19df-4905-8a26-118546c7f8a7', '2fc8e9b6-449e-4652-b92c-c582d0f24ad8', 'IMAGE', 'https://cdn.chotot.com/8-W-RraO3r3FxZq9nIsUEnGBK-IETFw-75W-0tR7O3A/preset:view/plain/c42fcdb4d887d7033852ce91bd6f6a54-2994587427493112065.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('447c583f-e4fc-4258-aea4-84e0f0e0325e', '2fc8e9b6-449e-4652-b92c-c582d0f24ad8', 'IMAGE', 'https://cdn.chotot.com/dKN-fjXdeoWfI2oCrhHbexURjKp_b7aNe30PLy1Q53Y/preset:view/plain/33c7a3f33d1452abeebf64ee4924944c-2994587432673630311.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ff9a924d-df6d-4bf2-9020-e8bb21e9826e', '2fc8e9b6-449e-4652-b92c-c582d0f24ad8', 'IMAGE', 'https://cdn.chotot.com/NkqtmNA8UGnUOjspYS3donA3V6QEKnUfkoDi08FVL9Q/preset:view/plain/518fd1980d80c7cb92bb4f4f2fc87989-2994587432424645947.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('840cd005-6366-415d-a9e4-1bc9bfc595ab', '2fc8e9b6-449e-4652-b92c-c582d0f24ad8', 'IMAGE', 'https://cdn.chotot.com/tiJ27dN86q2AZvCdyzRAES86CVlcgjFx-pPAnGBukxI/preset:view/plain/cddcc749ac6e424b7fcc2214b6a3c0d2-2994587429983732314.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('56663da3-73f8-446e-8738-cf9c21349469', '2fc8e9b6-449e-4652-b92c-c582d0f24ad8', 'IMAGE', 'https://cdn.chotot.com/RknwRkA3LkgUDTg6EHSYwkOuJ2wTtYMCqVNYZih_UE4/preset:view/plain/d1ebcc8d76320df5f6e94da14c479243-2994587432623507364.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2c22a3dd-0271-4191-ac8a-16022f800d18', '2fc8e9b6-449e-4652-b92c-c582d0f24ad8', 'IMAGE', 'https://cdn.chotot.com/icELupB5pJnjYPM4TF3Yjq2q8p6_YNw6EzIlD5CS7rs/preset:view/plain/5eb4d3aa4978d9ff1deab0aa1917ca8a-2994587429489666305.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('281f44f6-a180-42b5-83c4-ea91e8176e87', '2fc8e9b6-449e-4652-b92c-c582d0f24ad8', 'IMAGE', 'https://cdn.chotot.com/LlxB8nScBV9zZSeteEP3SizEw24FHRaBIVhNGRrfEPA/preset:view/plain/fa7f4af3eec4a2c945599bc94aac38c2-2994587429441229680.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3cc29909-23b5-4c15-b208-acc15284c901', '2fc8e9b6-449e-4652-b92c-c582d0f24ad8', 'IMAGE', 'https://cdn.chotot.com/rG13G3QSm2VXlKjkS5ZNVZeeUPfa6y7bkhLauBdIawQ/preset:view/plain/1adf6904dd0d8b1635e43125ce875a17-2994587433686476485.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('5ed4bbe9-e9f3-4076-a20a-f37fb8042514', 'P_133697777', 'APARTMENT', '✨ Khai Trương Studio Mới Tại 29 Yên Thế - CÓ BAN CÔNG – FULL NỘI THẤT ', '📍 29 Yên Thế, Tân Bình
Giá: 6tr3-7tr5 (ban công riêng)
Ban công riêng đón nắng và gió tự nhiên.
✨ Full nội thất, chỉ cần xách vali vào ở.
✨ Gần Sân bay Tân Sơn Nhất, CT Plaza, Công viên Hoàng Văn Thụ, Pico Plaza, Công viên Gia Định.
✨ Thuận tiện di chuyển đến Phú Nhuận, Gò Vấp, Quận 3 và trung tâm TP.HCM.
✨ Tòa nhà an ninh, giờ giấc tự do.

📞 Hotline/Zalo: ***
📩 Liên hệ ngay để nhận ưu đãi và giữ phòng.', 'UNDER_OFFER', 'Quận Tân Bình, Tp Hồ Chí Minh', 30, 6300000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('84cb74ed-e6d3-4652-a3fd-09f259466ae2', '5ed4bbe9-e9f3-4076-a20a-f37fb8042514', 'IMAGE', 'https://cdn.chotot.com/u023hgbK7YkOWGeDCcZ88LdHLe9RXyPlKLUao6Jg39g/preset:view/plain/acbafcc2d5da53af240ddea12727189f-2994255764740352611.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('331f1338-147a-4459-97f3-3ce679b89165', '5ed4bbe9-e9f3-4076-a20a-f37fb8042514', 'IMAGE', 'https://cdn.chotot.com/CWSL8emI3ogbKQgXt2ppXTTJc8WlZtVxN814QxldLcw/preset:view/plain/4975f594921e7f0902a9af26a5c6fc84-2994255764403768189.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('31086b39-02c6-44d1-86b4-757ee047e6e7', '5ed4bbe9-e9f3-4076-a20a-f37fb8042514', 'IMAGE', 'https://cdn.chotot.com/p6f2gyC_8gFYEBmPTOqrYUzOZEZrnHGoQcBG1ruoUbA/preset:view/plain/7dfd46b57f2cb145c97926110ab35e31-2994255764154391749.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3266ab1d-10a4-41b0-8d0d-cc06620cce4e', '5ed4bbe9-e9f3-4076-a20a-f37fb8042514', 'IMAGE', 'https://cdn.chotot.com/LeQiYAed7dLCzI8_2IcI3qx9el4NOVoaled2q8oWJcI/preset:view/plain/0947ee8707e436dda4f1b92f55add45f-2994255764338193071.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a6cf989c-92c8-4460-8db0-43bba4ba1682', '5ed4bbe9-e9f3-4076-a20a-f37fb8042514', 'IMAGE', 'https://cdn.chotot.com/zc5cBEAV15bqbwyU6y4ELehw8frpNTATSQlLxGLFmcE/preset:view/plain/1c6b8f95f5fc217247bdf5ae8c0fe618-2994255764008379713.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('eb7f2de0-1890-4ca4-9e87-37fbcd549658', '5ed4bbe9-e9f3-4076-a20a-f37fb8042514', 'IMAGE', 'https://cdn.chotot.com/O8X5cEQoUYDG08Zb7dCHEjVkz9MbzGfrL0ilmUbUTcY/preset:view/plain/30ad807c318ea325a90ea770f8d3b222-2994255764496939150.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0b731ec6-af40-4890-91cd-8a4358e58e1d', '5ed4bbe9-e9f3-4076-a20a-f37fb8042514', 'IMAGE', 'https://cdn.chotot.com/z5jSV_IiDzBvPkRa9B3sXzMNeTDT0VsBb-D12FaTouQ/preset:view/plain/65f6c4deed051d4a4c665617e8addc86-2994255764857619636.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('db6dc69c-5a89-4f3b-9830-ab30c1614065', '5ed4bbe9-e9f3-4076-a20a-f37fb8042514', 'IMAGE', 'https://cdn.chotot.com/vS_GG4cMaN21W6385d3-7klT1rQtUXGGs8LA6KTv7_s/preset:view/plain/09dc96932027849628b3b023ba50a151-2995403675239860601.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ca5446ec-4e2e-42e4-aaca-2c5eaad98ef4', '5ed4bbe9-e9f3-4076-a20a-f37fb8042514', 'IMAGE', 'https://cdn.chotot.com/QHvc-I8ytTez381LAe6bza65hhA4MnNR7BQuc0gojvM/preset:view/plain/17554eb87ac8f1d709aebdfe8e0533af-2995403675531722914.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0e71648d-a1ca-4984-b923-e895dc9f74d4', '5ed4bbe9-e9f3-4076-a20a-f37fb8042514', 'IMAGE', 'https://cdn.chotot.com/BMd7SNcF0O3XXvzjeoakf7azHd5lYtJcAe8huiSQ4ho/preset:view/plain/ae892c1e09b74be8d2352dc7ff002bf4-2995403675412124042.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('25d00d12-dd31-405a-9490-55a628b16796', '5ed4bbe9-e9f3-4076-a20a-f37fb8042514', 'IMAGE', 'https://cdn.chotot.com/a_t1m3WJfv9mX2cvyfRtr34mO2vMLlC_iR-k5hW6aa4/preset:view/plain/cbdf903abbf722ea064d50e36a3aee68-2994255764150033301.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('472f976c-a6e7-4092-9553-964046475f03', '5ed4bbe9-e9f3-4076-a20a-f37fb8042514', 'IMAGE', 'https://cdn.chotot.com/8e5koIPj8E6SsXkpLZnQYUGl5JvzzQHb_x4IU19pV5g/preset:view/plain/9f1fd1877aa28d0d34a74ebd55eec205-2995403846755470705.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('82d6b504-3f6e-4a34-b6ec-88e051ac122e', 'P_133941251', 'APARTMENT', 'cho thuê căn hộ hạnh phúc, full nôị thất, 2 PN', 'Dự án: 
Thông tin chi tiết: Cho thuê căn hộ happy city
Căn góc, full nội thất, tầng cao
63m2, 2 phòng ngủ, block A
Giá: 7tr/tháng 
Liên hệ xem nhà thực tế 
***', 'SOLD', 'Huyện Bình Chánh, Tp Hồ Chí Minh', 63, 7000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b9521deb-3fdb-4642-bec4-b32ac76d40a2', '82d6b504-3f6e-4a34-b6ec-88e051ac122e', 'IMAGE', 'https://cdn.chotot.com/Xokap8oc5SsI7ktE6Se4rMWWO4RZXZs6Sr8Vtf1p7Hs/preset:view/plain/d56668c87ba834503da84ed95b346425-2996124806304998436.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('11c15da1-6ba6-4dc7-bbc8-50d19b354705', '82d6b504-3f6e-4a34-b6ec-88e051ac122e', 'IMAGE', 'https://cdn.chotot.com/Ogaij1dtLuxUZqIquxk9xE5lQAEtwDfpY6QJJt3021M/preset:view/plain/b82795454ae12c899b88e10bf816c75f-2996124803540207993.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a8028b6c-7652-4134-b19f-4b534a946a7d', '82d6b504-3f6e-4a34-b6ec-88e051ac122e', 'IMAGE', 'https://cdn.chotot.com/0d1ISHRFUdgl0wAqQXSSm7nvwYrAnGEs3alN22RAJ9s/preset:view/plain/fd3f3e0a18639a885f7caac375ebba41-2996124806711430759.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('4ccfea49-5875-4c6b-9a71-40c10786b318', 'P_131899766', 'APARTMENT', 'CC DVELLA 2PN2WC Cho thuê sát kcx phú mỹ hưng cresentmall thuận tiệnq4', 'Dự án: 
Thông tin chi tiết: CHUNG CƯ DVELLA
📍Vị trí 1177 Huỳnh Tấn Phát
An ninh đầy đủ tiện ích
Có Gym Bơi 
Free các tiện ích toà nhà
Điện nước nhà nước
KDC An ninh
Có thể nuôi pet
xe 100k/c
Pqly: 9k/m2
————————-
zalo/call: ***', 'SOLD', 'Quận 7, Tp Hồ Chí Minh', 70, 10000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5507d24c-f2e0-4d23-91ee-640198b74fb7', '4ccfea49-5875-4c6b-9a71-40c10786b318', 'IMAGE', 'https://cdn.chotot.com/LU8r08cDvdUN3See9TiyMqelAJ3l6MUwr-bWUihn0-I/preset:view/plain/f8e7b4daa81f211ab61156a30c053350-2980456159771195576.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e729860c-2b47-4c57-920f-66e70670d244', '4ccfea49-5875-4c6b-9a71-40c10786b318', 'IMAGE', 'https://cdn.chotot.com/nvWpLYA8xwc-BhBn4H1WE70ytS7oUrOppW8IwSbUQAU/preset:view/plain/baf7db67b6f83c390fe702898b110d82-2980456159749139217.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ed9b2e40-8f40-4b2f-94c2-81904bbb3225', '4ccfea49-5875-4c6b-9a71-40c10786b318', 'IMAGE', 'https://cdn.chotot.com/_-hZ-ScZbf5WytcoZCCFuXAFmUfI9KPYhyf8iNdLbuA/preset:view/plain/4602db94d614fbd86fb9b1495ebcf07d-2980456159914892312.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c9bb0432-4f56-4fac-abe2-14fb21c8f147', '4ccfea49-5875-4c6b-9a71-40c10786b318', 'IMAGE', 'https://cdn.chotot.com/vGibNF9AFVMYZjQvI4ZFCXSzq-BuY2m3S4WJcXaTObE/preset:view/plain/42647e63e16cc3fefde1ee19cf9b0513-2980456159835357973.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9b8c2107-fde8-493c-be6a-051530033ce6', '4ccfea49-5875-4c6b-9a71-40c10786b318', 'IMAGE', 'https://cdn.chotot.com/Gza-8qfR4Vl5LLqxhKhf23rRIg-N2veuor7jfR_vBQo/preset:view/plain/72ffd2a42968203cd05233b4d57cff07-2980456159951072515.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8b7bf562-3636-4c54-b277-d498eb2eff68', '4ccfea49-5875-4c6b-9a71-40c10786b318', 'IMAGE', 'https://cdn.chotot.com/syTRNT1dEVffWHThME3elzdLUgpn2bVWbwCKNLRTivA/preset:view/plain/c7f22fedaeed49b8d73e8349fb641c9e-2980456160093768937.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('63bc9712-7ec4-42e8-8fdc-3f47b935e0f4', '4ccfea49-5875-4c6b-9a71-40c10786b318', 'IMAGE', 'https://cdn.chotot.com/dhb9p-JoOSrGCggqa_Ysi4ax_I3_8dy9yS_VqoVzh4k/preset:view/plain/fc1f833d2db7393f95346a4ae8758d43-2980456159067175978.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('c8320620-a483-496c-b665-d8f15cb7ca30', 'P_131735171', 'APARTMENT', 'STUDIO BAN CÔNG XA BẾP CỰC RỘNG GẦN MŨI TÀU ÂU CƠ & TRƯỜNG CHINH', '- Vị trí thuận lợi ngay mũi tàu Âu Cơ & Trường Chinh, Lũy Bán Bích, Tân Kỳ Tân Quý, Big C Trường Chinh, Nguyễn Văn Săng,…..
- Toà nhà 4 lầu, ra vào vân tay, xe để trệt, camera 247, ko chung chủ
- Nhận khách DÀI HẠN, NUÔI PET, NƯỚC NGOÀI
Ngoài ra, với gần 4 năm làm việc trong lĩnh vực này, mình còn giỏ hàng nhiều căn, nhiều dạng khác nhau khu vực Tân Bình, Tân Phú và lân cận. Hãy vào CHUYÊN TRANG của mình để tham khảo nhé.', 'SOLD', 'Quận Tân Bình, Tp Hồ Chí Minh', 35, 5500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('01024625-348d-4b74-9de6-a5df58634ea2', 'c8320620-a483-496c-b665-d8f15cb7ca30', 'IMAGE', 'https://cdn.chotot.com/FPGQwa4V5tWbMl55FRzvyiqxAfB88naABeZ8kZwVXbM/preset:view/plain/f947efcdbf25649235e2e587b73b617b-2995723939190654436.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4d5da654-c1e8-414d-abcb-3bcc7ec9aaa7', 'c8320620-a483-496c-b665-d8f15cb7ca30', 'IMAGE', 'https://cdn.chotot.com/DbnyBB7saSp2T3ce3DxWO5tex09YWGfhZtPbx3Y3SEI/preset:view/plain/80001cb391cd6124f4e9d481ab1845d2-2995723939783329345.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('43ea3923-a4c1-4cb4-bcb3-cd081f72724e', 'c8320620-a483-496c-b665-d8f15cb7ca30', 'IMAGE', 'https://cdn.chotot.com/FLUL3y7i57E-Cu_7EjgMoSoPU6HFNamZfi_ZNFEsrSQ/preset:view/plain/324a3adf7655dda70737d534e246471b-2995723939299740025.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8c075446-af08-4dd9-bda5-a96a31a43742', 'c8320620-a483-496c-b665-d8f15cb7ca30', 'IMAGE', 'https://cdn.chotot.com/2eHZ9hgJuNW3kta61ef9xdbUU3hUZIgdaPYNxmLkoBI/preset:view/plain/f64462ce85f540e5e72a94d5a567c2c2-2995723939744660556.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d8b9c0db-7746-498b-abdf-f785d090f910', 'c8320620-a483-496c-b665-d8f15cb7ca30', 'IMAGE', 'https://cdn.chotot.com/IUC7g1b2L76ouP9Oa40OFX6MWD__4lMQ7HOafV-AW5I/preset:view/plain/eab680a590c401e587121cc46aae346c-2995723939602082007.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4a89805a-bca9-4ea3-bc15-20e650843e3a', 'c8320620-a483-496c-b665-d8f15cb7ca30', 'IMAGE', 'https://cdn.chotot.com/Z59DIVuZP2wCNCl0p9RG_alM83kAxbT2hJVc0jAdfhw/preset:view/plain/c9edb39cf1e0b6bfac26a5440bc81dc7-2995723939941510258.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9db3e67d-768a-41b0-89cd-e73b548dfd3f', 'c8320620-a483-496c-b665-d8f15cb7ca30', 'IMAGE', 'https://cdn.chotot.com/sNowv2ag4Yw3gx9_BR6Ni78fzPu5lcVD5KIAGBM28Z8/preset:view/plain/3b8e14581ea3cb35a19637cb7dd0f09b-2995723939852384698.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('12a02dc9-5366-4658-84b3-6b5f1d580def', 'c8320620-a483-496c-b665-d8f15cb7ca30', 'IMAGE', 'https://cdn.chotot.com/PQWQVUa3DXZ4oTXlWfX98yuDPSQkTzi6f-JuHlJEFAw/preset:view/plain/61cc865a20146ce1e63966ae1052f035-2995723940053372514.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cb8e12bf-63ca-4564-b233-e42e9a50f53d', 'c8320620-a483-496c-b665-d8f15cb7ca30', 'IMAGE', 'https://cdn.chotot.com/ZGECKLvS9UDEJXnqJkILjWypl0naAc70xxtXZI-BhCg/preset:view/plain/47500f19f718451f7cfc5c9883204b6a-2995723939872544162.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ae693ff7-ac94-49cd-a3bb-dd3a6a58b4ba', 'c8320620-a483-496c-b665-d8f15cb7ca30', 'IMAGE', 'https://cdn.chotot.com/NBncq_z0Zr49M1aswOj3deAc4gBkaAmY8I4PoVapl_U/preset:view/plain/3c167cf10786f3c9dfe7f18da195f976-2995723939925718150.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f598594f-0d88-46d7-81d0-b6916a6729a7', 'c8320620-a483-496c-b665-d8f15cb7ca30', 'IMAGE', 'https://cdn.chotot.com/UuqAJEkUjTXA-Ov9lkp5GAAYyGJB65u_-Y3r0BXKThM/preset:view/plain/1e315f57a0f6a01428663b915972ed93-2995723940506188714.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('98c7eced-ed61-4e1c-8047-a2939e13b965', 'P_133928639', 'APARTMENT', '🔥Căn Hộ 1 Phòng Ngủ Tách Bếp Cửa Sổ Thoáng Ngay Lê Văn Sỹ Đặng Văn Ngữ', 'Dự án: 
Thông tin chi tiết: Tiện ích toà nhà:

+ Toà nhà với nhiều tiện ích chung, có người lau dọn hành lang bãi xe khu vực chung, có khu giặt sấy, có thang máy, bảo vệ

+ Phòng được trang bị đầy đủ nội thất gồm: Máy lạnh. Tủ lạnh. Giuong nệm. Tủ quần áo. Kệ bếp. Tủ bếp. Máy nóng lạnh,...

+ Hầm xe toà nhà rộng rãi, ra vào đi lại tự do, camera bãi xe hàng lang 24/7, trang bị pccc đảm bảo an ninh.

+ Khu dân trí cao an ninh, gần các cửa hàng tiện lợi, trung tâm mua sắm, khu sân bay, BV Tâm Anh,...

+ Thuận tiện di chuyển đi các địa điểm: CV Hoàng Văn Thụ, Vòng Xoay Phạm Văn Đồng, Vòng xoay Lăng Cha Cả, Dễ đi Quận 1 - Quận 3 - Quận 10 - Phú Nhuận - Gò Vấp - Binh Tân,...

Liên hệ: SĐT - Zalo - FB (Thái Thịnh).

Hỗ trợ tìm phòng và xem phòng khu vực Sài Gòn', 'UNDER_OFFER', 'Quận Phú Nhuận, Tp Hồ Chí Minh', 30, 5000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5955f8c6-94fc-4603-9d37-17ffce54bda8', '98c7eced-ed61-4e1c-8047-a2939e13b965', 'IMAGE', 'https://cdn.chotot.com/yUlG75X_Y8zvh3zOQPcHL5esKpKsdg6YwjGs6e9HDr0/preset:view/plain/b6bdc56c26ace91758bde1573f20ea48-2996020780546014313.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('35d7538f-3d78-42ae-a6d2-88959192f9c2', '98c7eced-ed61-4e1c-8047-a2939e13b965', 'IMAGE', 'https://cdn.chotot.com/92EYJJv51L4zFAfNTJva7c-TIPmmCblvV5dwrPO2tEY/preset:view/plain/592a64a10d93928c88d69976e9623414-2996020780558300521.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('27b2f143-bcb3-4249-8e2e-26725b5c734d', '98c7eced-ed61-4e1c-8047-a2939e13b965', 'IMAGE', 'https://cdn.chotot.com/fWS5yOyKd6tDQBgu1krxAYLKMwhAQ3D1EI7ktK2AVyM/preset:view/plain/3c645c7236832273ab3a481fdf6b8cc0-2996020781087773695.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('45afcd1f-b22c-4939-8a43-94dd1cd4f1f2', '98c7eced-ed61-4e1c-8047-a2939e13b965', 'IMAGE', 'https://cdn.chotot.com/UP7sgxvNWVuSNqL-OMREwWJLqW5XqYX4j74SN_7UyaU/preset:view/plain/9936133af39f412d82086546de80c67b-2996020780679957076.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fd14f133-91c4-4980-b36d-0f61b19c797f', '98c7eced-ed61-4e1c-8047-a2939e13b965', 'IMAGE', 'https://cdn.chotot.com/rfrUVrtMp4d1qVJAiCFY7fxTp_fea81LmqtFEmFU1Ns/preset:view/plain/edf2ea753a7b8db9ceb772519b31f90e-2996020780745902457.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8a612341-41bf-469f-af31-66ea714c2e79', '98c7eced-ed61-4e1c-8047-a2939e13b965', 'IMAGE', 'https://cdn.chotot.com/_UIXoYjEP2QKU4tpmn9M7rjjTZwXA7jCVoWtldmVyJI/preset:view/plain/d75d1e412d9ca66d7426a8a4df72ce26-2996020781066472840.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f2f1b2b8-28ff-41d0-a285-44f5c694f176', '98c7eced-ed61-4e1c-8047-a2939e13b965', 'IMAGE', 'https://cdn.chotot.com/fuYjGvR7khsrXBSQQvtztiGWdXFteTm7lHC7c2XYHM0/preset:view/plain/161f7ec585827a94d6716a4f17df74a0-2996020780717622756.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1c08f374-77a4-4c54-8394-e6808343d451', '98c7eced-ed61-4e1c-8047-a2939e13b965', 'IMAGE', 'https://cdn.chotot.com/PYjfOxXKw-dy8xvW7h9pHr2d3KXESfm5_ViJq-yfM04/preset:view/plain/d0e43050b9e60ff02a3a48b500789f85-2996020780794851519.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('5e4d39a2-e738-4a93-841e-b58ac82b3250', 'P_133899470', 'APARTMENT', 'STUDIO CỰC XINH CÓ BAN CÔNG NGAY LOTTE MART', 'Dự án: 
Thông tin chi tiết: Căn hộ cực thoáng nằm ngay vị trí gần sân bay T3 tiện đi lại Tân Bình- Phú Nhuận - Tân Phú.
Ban công thông thoáng gần các tiện ích chợ , quầy thuốc , khu ẩm thực . PCCC an toàn xem phòng liên hệ ***', 'AVAILABLE', 'Quận Tân Bình, Tp Hồ Chí Minh', 30, 5500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('99775d29-1a2a-4f85-813c-9449c37a05db', '5e4d39a2-e738-4a93-841e-b58ac82b3250', 'IMAGE', 'https://cdn.chotot.com/eAPWuQgBnLcDMrQlhHyCVVjDLp0QLS9Gh2bDbzxqI10/preset:view/plain/39e070d8d484268b1926fa4eb2be5f1a-2995812405462899265.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2b900931-9241-4948-887c-c07148840f01', '5e4d39a2-e738-4a93-841e-b58ac82b3250', 'IMAGE', 'https://cdn.chotot.com/SojZQiKVUNti3pkvxMf5ddkjkOT9e5ujVlp1O4-ULw4/preset:view/plain/09fb2ee6e4329810d1fd78b02d31d764-2995812406497990307.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('df4fc8f4-1214-4a3f-ad74-501082a4c69a', '5e4d39a2-e738-4a93-841e-b58ac82b3250', 'IMAGE', 'https://cdn.chotot.com/bTME3NDM_jpFf8qAZbuzNzEpya1xGitSl-U6OeZnvnA/preset:view/plain/7c9a5213cf6952dc9cb8b6ab7bcd4323-2995812406863923796.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('55ef3c57-bb8c-42e3-9807-17cf825bba90', '5e4d39a2-e738-4a93-841e-b58ac82b3250', 'IMAGE', 'https://cdn.chotot.com/mGREN2bMmAJLvLpghlmL-kGls5EgLO5pCBRHfYThGlY/preset:view/plain/b0406cccf3605d899783f2d229579441-2995812406209849189.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('08645811-cc08-45d8-ae74-9015382f85a9', '5e4d39a2-e738-4a93-841e-b58ac82b3250', 'IMAGE', 'https://cdn.chotot.com/CUAyKmp2ongm-dY2E1SUNUxP9wn_pk6W48MUhC9U0GM/preset:view/plain/3d6bbf2386248e3ef5037fb39ed80e22-2995812407325235777.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e7f93180-1c81-4606-af5e-bb5832c0a8fa', '5e4d39a2-e738-4a93-841e-b58ac82b3250', 'IMAGE', 'https://cdn.chotot.com/sp92VoLLVRNA2CRjTfsM8396WaihyERgeU_erALM6qM/preset:view/plain/f39523c686d84336e93cd5a970041ffa-2995812407554799417.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('254703a2-7700-460a-aeae-d2f38e0e6c06', '5e4d39a2-e738-4a93-841e-b58ac82b3250', 'IMAGE', 'https://cdn.chotot.com/221q9cwl_DvGQy5GQlH-vFdgw-9NV8yaqJNyKRqbxgk/preset:view/plain/28a4eff1f4f7d4c8cc616af6e79df13b-2995812407705719549.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('60550e0c-0e60-41f0-8c66-933bfee6b513', '5e4d39a2-e738-4a93-841e-b58ac82b3250', 'IMAGE', 'https://cdn.chotot.com/D_ShVsLAdWoGnUbYjdHTOv6S2WDaFFZyhlj-VB_YHfE/preset:view/plain/637f23a1aa5e58dad73e8a8c1346aa00-2995812407554834115.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ff273a19-75e7-4330-ae29-4253fbe10726', '5e4d39a2-e738-4a93-841e-b58ac82b3250', 'IMAGE', 'https://cdn.chotot.com/wrl_09GDxTCprli1gmpYqEWY56IRuS2WqFFKm50RLRg/preset:view/plain/4ad6e108fcf3a4aed153a6e35f71d111-2995812407817848292.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cfdf50f2-6f17-49e1-b398-33d0c8bdfd79', '5e4d39a2-e738-4a93-841e-b58ac82b3250', 'IMAGE', 'https://cdn.chotot.com/AcxmGF2gnCDDTaci54XGOksC0guuO7DLa20cNWOt5SE/preset:view/plain/fb47adeb839c4e03c750f44b5c4f5fae-2995812407644307524.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('311be1fa-c6bb-4053-8f69-2e21c88aba14', '5e4d39a2-e738-4a93-841e-b58ac82b3250', 'IMAGE', 'https://cdn.chotot.com/X-5t9oGGKXmHWZkP_ghr2Op9r67q9z_F1KqGZFYYIp8/preset:view/plain/112a9b6b3b5d620902a396f0666e6049-2995812406746226356.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('33e92fd2-30db-412a-b67d-42e38b3cfd67', 'P_133941224', 'APARTMENT', 'Căn hộ Thủ Đức giá rẻ 2PN 2WC chỉ 970tr nhận nhà ở ngay Full nội Thất', 'Căn hộ Thủ Đức giá rẻ 2PN 2WC thanh toán chỉ 970tr nhận nhà ở ngay Full nội Thất.
Vị trí: Mặt tiền Tô Ngọc Vân, Tam Bình, trung tâm Thành phố Thủ Đức 
Vị trí Vàng kết nối đến Vành đai 2, Vành đai 3, Tuyến Metro số 1 - Bến Thành - Suối Tiên thuận tiện đi lại.
Căn hộ 2 phòng ngủ - 2WC diện tích từ 53m2- 68m2 phù hợp cho các gia đình từ 2 đến 3 thế hệ.
Nhận nhà ở ngay vào tháng 9/2026 giá chỉ 2 tỷ 870tr/căn
Dân cư hiện hữu đông đúc, dịch vụ tiện ích đầy đủ trong bán kính 1km đầy đủ: Trường học, siêu thị, bệnh viện...
Thanh toán chỉ từ 30% nhận nhà ở ngay
Ngân hàng hổ trợ vay 70%, lãi suất ưu đãi 0%
Chi tiết liên hệ ngay em Hoa để xem nhà mẫu và chọn căn ưng ý.
', 'SOLD', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 59, 2870000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('94e6d7f3-7265-4f9a-9cee-1eaf00c725ea', '33e92fd2-30db-412a-b67d-42e38b3cfd67', 'IMAGE', 'https://cdn.chotot.com/DCcJOXI4WNLtubBZyIFtLpatixmg-bhKoX09IK4yf_0/preset:view/plain/c3b5d8c9a8e9bbb96ddeba609ee9c6b4-2996121414688979693.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('481a4908-3716-4fde-af6c-24e5837beaed', '33e92fd2-30db-412a-b67d-42e38b3cfd67', 'IMAGE', 'https://cdn.chotot.com/Kvz7LwbbeIPKOLmPw4NbJYwZ9vfVnmtko8u_3wPitoY/preset:view/plain/0d179c86d184ca5d252b0b57c04b0ee9-2996121427238241764.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d83d791d-3f8a-46d0-bdef-9c0c1a1c68c9', '33e92fd2-30db-412a-b67d-42e38b3cfd67', 'IMAGE', 'https://cdn.chotot.com/Xw6ZqesmbsKdAbzg5LuzsrUluU8uB8wDeqVJSe782yU/preset:view/plain/821b171628675b4499f42465e745492a-2996121441945818408.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('389ecb12-af8c-4237-aae0-324cb2bccc68', '33e92fd2-30db-412a-b67d-42e38b3cfd67', 'IMAGE', 'https://cdn.chotot.com/xox2q4-4fkxdiaClb9bHJXQu6kU5mmb-a93-d8lyxqQ/preset:view/plain/04a1e2acdbcf94c78d2a6067356099f3-2996121455584400383.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('01d6dc08-5949-4158-9200-2f2d25196b98', '33e92fd2-30db-412a-b67d-42e38b3cfd67', 'IMAGE', 'https://cdn.chotot.com/OTANf3LhoGz0-kW8U55O3zAIa0-ymvsO9nz11R-4z0w/preset:view/plain/0fc7beacbad414e194244684a356dcb8-2996121488486736932.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('bf99fcac-8bee-4bfb-ab96-fcf31828edda', 'P_130606482', 'APARTMENT', 'GIÁ *** THÁNG 6 ECO GREEN NTCB CHỈ 13TR - FULL NỘI THẤT 15TR', 'Hi mọi người, em đang có list căn 2PN2WC  giá tốt hơn thị trường, nhận nhà liền:

🏡 Căn 2PN2WC 70m2
• Giá: 13/tháng - NTCB | 15tr/tháng - full nội thất
• View thoáng, tầng trung – cao, vào ở ngay
Liên hệ em qua hotline để trao đổi', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 70, 13000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0be8ab85-70fa-4b39-96d4-b4cb782d6278', 'bf99fcac-8bee-4bfb-ab96-fcf31828edda', 'IMAGE', 'https://cdn.chotot.com/_sa4gLiAxQuLlR7WSCyvoS69syvCuviwYK1hhbaiAME/preset:view/plain/8003e7e1303fc3271c9cb1c569bbb4ed-2969460131399795226.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('54fbecd8-a901-4d8d-b0de-5cc2dd7aa709', 'bf99fcac-8bee-4bfb-ab96-fcf31828edda', 'IMAGE', 'https://cdn.chotot.com/94KY-vKiia6sxLwncEUF0fPLIvgg2_wYICpQSBAF5_w/preset:view/plain/ce539695b8095607cd230dbf1d2975cf-2969460131437409335.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6bed5503-74c5-49bf-a3fa-e446cb440045', 'bf99fcac-8bee-4bfb-ab96-fcf31828edda', 'IMAGE', 'https://cdn.chotot.com/f0C5E8j7YeVJuijt_MFNoVLHRBULObsAG5GwNpYm8Cs/preset:view/plain/83dd46b2e0536467bcbac98be131c55c-2969460131241999861.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3c42a95c-9ffb-4a4f-b533-cec3a5885ff2', 'bf99fcac-8bee-4bfb-ab96-fcf31828edda', 'IMAGE', 'https://cdn.chotot.com/I0VWBPu2H_NFj92SMqid7GsmevSb8r4Uo4z-M4MOdEk/preset:view/plain/201cfc2413fe2d19dcfd3cb7bb1a7171-2969460131401556306.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b9e86f30-a7fa-44b1-a519-5a1a6c709b2f', 'bf99fcac-8bee-4bfb-ab96-fcf31828edda', 'IMAGE', 'https://cdn.chotot.com/CahfUcTfHBiCUZmLtOn7zlLAgtMTclLJ82tKP0X8kE8/preset:view/plain/a4f438bee9a555b8bfd85b885a77fe2f-2969460131856715479.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bddfaaa1-1059-462f-9da1-739ba9656fcf', 'bf99fcac-8bee-4bfb-ab96-fcf31828edda', 'IMAGE', 'https://cdn.chotot.com/AnqQSjUuyGNXRo8gi2brN8twGybeJ0MJIk_w3jLkEzs/preset:view/plain/2ca3e5bcd9163ccb9c7356afe4c48b35-2969460131189694063.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('020dc175-48ba-4d10-8001-4c999765beb5', 'P_133941217', 'APARTMENT', 'Cho thuê căn hộ Akari City 2 Phòng Ngủ 1 Nhà Vệ Sinh', 'Dự án: 
Thông tin chi tiết: Cho thuê căn hộ Akari City.🍀

Địa chỉ: Dự án Akari City, Số 77 Đại lộ Võ Văn Kiệt, Phường An Lạc, Quận Bình Tân, TP.HCM (Mặt tiền trục lộ lớn, di chuyển thông thoáng, không lo ngập lụt).

2 Phòng Ngủ 1 Nhà Vệ Sinh 
diện tích 61m2
full nội thất cao cấp
Giá Cho thuê: 12tr
chủ nhà bao dọn phòng 1 tháng 1 lần ạ

SĐT Liên Hệ Zalo:***.📞', 'AVAILABLE', 'Quận Bình Tân, Tp Hồ Chí Minh', 61, 12000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('71c153c9-5e96-436a-8d10-96a2217cd669', '020dc175-48ba-4d10-8001-4c999765beb5', 'IMAGE', 'https://cdn.chotot.com/zRV4M8s-ppghrSF9Y68ObEvwbJu-S66njAN4SctiYaw/preset:view/plain/66f58d8aa691543b501833034a45b6a0-2996124234857491383.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5c5497ef-3b7c-441a-907a-a4d428377959', '020dc175-48ba-4d10-8001-4c999765beb5', 'IMAGE', 'https://cdn.chotot.com/qseSAeQLrKXBWYZVn76X6E4Lt3AkLCHJVT5-VWS4Hk0/preset:view/plain/5d04716a7f4fd0744e48912aedb541c0-2996124234901460264.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e372c996-2d29-4c91-b036-96cd8b08c808', '020dc175-48ba-4d10-8001-4c999765beb5', 'IMAGE', 'https://cdn.chotot.com/Z2Qzoo91gGCZRWdyeOnnAfQYoCsS4bv7-y4GROS6Sig/preset:view/plain/5123784aecc94fbc97668cde38f24cb6-2996124235301639167.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('06107f0e-55f6-438f-916a-530bbe386d3c', '020dc175-48ba-4d10-8001-4c999765beb5', 'IMAGE', 'https://cdn.chotot.com/oYzh6fx5c-cU78zb7bYcetgq9LEZu8IKtzu8zcCQ3wo/preset:view/plain/6330d7540b5039ec49d83cdd2277ee89-2996124235588192633.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4ae8c08e-e777-45ca-b687-0876f8810dc8', '020dc175-48ba-4d10-8001-4c999765beb5', 'IMAGE', 'https://cdn.chotot.com/-_3QamXksXQqt_iK7Ij6_1iD0x8yxpxd38JTdi4DB9g/preset:view/plain/85d523fe3982295fa30ac0352eb9ee00-2996124235595271783.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('82677746-0364-4a94-9027-93a34b9a8e25', '020dc175-48ba-4d10-8001-4c999765beb5', 'IMAGE', 'https://cdn.chotot.com/zZ32hDkwjkVNELHNLS5bFyfvb9h3PG7RjgEqM7DCcVk/preset:view/plain/afbf753289f297cc65c5f7ef786d3585-2996124235644388836.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('a8cf8b36-6c43-40d3-8d72-0d463c55dd4d', 'P_133941214', 'APARTMENT', 'Cho thuê căn hộ Diamond Riverside 2 Phòng Ngủ 2wc full nội thất gt', 'Dự án: 
Thông tin chi tiết: Cho thuê căn hộ Diamond Riverside 
Võ Văn Kiệt Quận 8 
2 Phòng Ngủ 2 Nhà Vệ Sinh 
Tình trạng: đầy đủ nội thất, nhận nhà liền được
Giá thuê: 11tr/th', 'AVAILABLE', 'Quận 8, Tp Hồ Chí Minh', 80, 10000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('42265579-b447-4792-a44d-0d6ce137c3e8', 'a8cf8b36-6c43-40d3-8d72-0d463c55dd4d', 'IMAGE', 'https://cdn.chotot.com/JIcQZfTuQPmMvpFMibfFAEiVPUetTbHcvcB3aU4fN2k/preset:view/plain/8a91bb22745f1d99ac7b4dd67402d40f-2996124647307646248.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('84a2ae47-4515-4014-aa12-2d8dd3611366', 'a8cf8b36-6c43-40d3-8d72-0d463c55dd4d', 'IMAGE', 'https://cdn.chotot.com/NBxZ5syYa41yI-7euF78q4LlIXsXpwO-SlbfICJ5kaY/preset:view/plain/d31c819a5ead34c5ecab4b44b6cec314-2996124647056558457.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9c2bd40f-5920-4693-87b2-08c3c9ef2bb7', 'a8cf8b36-6c43-40d3-8d72-0d463c55dd4d', 'IMAGE', 'https://cdn.chotot.com/MYhgSxlK4-c9PO54hGszHnN0Y2DQ4IqcaoIhUXMgBF8/preset:view/plain/69248f460cf65fdfb9dce5d86806fcb5-2996124647248074833.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c42c3606-7492-4f3b-979c-0a0e2ccd507b', 'a8cf8b36-6c43-40d3-8d72-0d463c55dd4d', 'IMAGE', 'https://cdn.chotot.com/mDlbOEp4bPyQI-OuGoqePy3WwTe9GqunxZlX6bzbcAM/preset:view/plain/b0d21c2fc175aa8c59f7e0b531c0d358-2996124647094207972.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fec2eab0-824a-41f9-9fa6-c25cebd79926', 'a8cf8b36-6c43-40d3-8d72-0d463c55dd4d', 'IMAGE', 'https://cdn.chotot.com/5diKE4aiA1AcAnFO3J9kR-iO2DSjGttpXRhkX-GppKs/preset:view/plain/d6695f4448111fa6f382c573408882f8-2996124647190658573.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0ced7f07-9cab-44f0-80c7-6437df4c2bf0', 'a8cf8b36-6c43-40d3-8d72-0d463c55dd4d', 'IMAGE', 'https://cdn.chotot.com/QH3Hy7mdAe5Aq49bw6huy4eDit7CNACgUmTdw9NJWS8/preset:view/plain/4c92167a7785bac65528391ed55a3362-2996124647156031576.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7f280ed6-2bce-4e99-9cee-fe66f1f69d4a', 'a8cf8b36-6c43-40d3-8d72-0d463c55dd4d', 'IMAGE', 'https://cdn.chotot.com/7knXjdux-QgqL1MmGDtSGHuz3lQ1aL5YHxSY7s6h4jE/preset:view/plain/6b1dff0758977945afc58a714006aaa1-2996124647122183204.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('220b1ce5-ce12-4124-835b-ac985b0fa22a', 'a8cf8b36-6c43-40d3-8d72-0d463c55dd4d', 'IMAGE', 'https://cdn.chotot.com/WIyrAqPCavvXGc3a6FiQLc3xzCRJBPoPtb7GU2TGxpk/preset:view/plain/8b7401f98ff0cd6d8fb88d096f0e82fb-2996124647267881983.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('8a9e8c2c-47c4-4505-86d7-ca0f35873a41', 'P_133941203', 'APARTMENT', 'cho thuê căn hộ block A, cc hạnh phúc', 'Dự án: 
Thông tin chi tiết: Cho thuê căn hộ happy city
 tầng cao 
Nội thất cơ bản: tủ giường, bàn ghế, máy lạnh
63m2, 2 phòng ngủ, block A
Giá: 6tr5/tháng 
Liên hệ xem nhà thực tế 
***', 'UNDER_OFFER', 'Huyện Bình Chánh, Tp Hồ Chí Minh', 63, 6500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c8daa230-cdff-4c84-8817-71a0b3d06061', '8a9e8c2c-47c4-4505-86d7-ca0f35873a41', 'IMAGE', 'https://cdn.chotot.com/2Ddmp-vGhEGQ1vrUDpkQAefclViy5IZ_Z6VcP0gJ6Zc/preset:view/plain/bc381c136d1737a11a9653071a6f616f-2996124363500112249.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('94c212bf-664d-438e-a3cd-26d1c6705e84', '8a9e8c2c-47c4-4505-86d7-ca0f35873a41', 'IMAGE', 'https://cdn.chotot.com/LXF3Nk3h0qFsuk87a12sh5otM6aQ-5vKVgxYJHwzqBY/preset:view/plain/6bb018eed496c36a3fb15a675cb535b5-2996124594073323897.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b0131011-d79b-4155-a2fc-72c2193c63fe', '8a9e8c2c-47c4-4505-86d7-ca0f35873a41', 'IMAGE', 'https://cdn.chotot.com/iakDycbHjMYwaJixlm-I8pwhPHtRepCM7-SxTR-J12Y/preset:view/plain/fa0d4241d106c9fedec78b80610bb8f4-2996124594127685092.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6c61e29d-4220-4227-a5f3-97191295376f', '8a9e8c2c-47c4-4505-86d7-ca0f35873a41', 'IMAGE', 'https://cdn.chotot.com/2TgViBNH5_DOja0BFsQI3z6_Py23qiiMFpwidIJbYO4/preset:view/plain/75e8ef9f3831450612e21c884383c453-2996124594196556727.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7ebd1a5e-0c63-4fa1-b657-09810e4f51f7', '8a9e8c2c-47c4-4505-86d7-ca0f35873a41', 'IMAGE', 'https://cdn.chotot.com/WlyoyUrWhJETGIJYy17q6injgkG_gLN_UG2iFBIwcuY/preset:view/plain/99c6866f9e8bf73de21e6dc7d293fd95-2996124593940568217.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('c31398b1-bf7a-449b-9da2-268144e9c82d', 'P_133399633', 'APARTMENT', 'Duplex_Gác Cao_Thoáng Mát_Tiện Nghi_Ngay Etown Cộng Hoà - Nhà Ga T3', 'Dự án: 
Thông tin chi tiết: 🏠 : Tiện ích xung quanh:
•Chợ, Siêu Thị, Trung Tâm Thương Mại
• Gần Trường Học, Khu ăn uống
• Khu dân cư an ninh, dân trí cao 

📍Tiện ích tòa nhà:
• Ra vào cổng vân tay
• Có bảo vệ, camera 24/7 
• Hệ thống PCCC đạt chuẩn
Liên hệ ngay để được tư vấn và xem phòng miễn phí!', 'UNDER_OFFER', 'Quận Tân Bình, Tp Hồ Chí Minh', 35, 4500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4cbbaa3d-c5c1-404c-b204-48d0134da4d7', 'c31398b1-bf7a-449b-9da2-268144e9c82d', 'IMAGE', 'https://cdn.chotot.com/o6ncPR2VsUCXlqbi6FRTPQ5ZgXopjloljF-7A7YRQhU/preset:view/plain/5c907750e9648073d47d00f03d98993b-2991978880274929828.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d650849d-f017-42cd-a4c6-60d6b340b6a8', 'c31398b1-bf7a-449b-9da2-268144e9c82d', 'IMAGE', 'https://cdn.chotot.com/TIqb_I9zZ_eWJVVaiFt5UA8UdGVDEYX9nJq4DxWbiis/preset:view/plain/7fde5660f9495e6a91d801e128f7b12e-2991978880268886393.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6d6d9b8c-ab15-4475-8aca-23ef4756cc4b', 'c31398b1-bf7a-449b-9da2-268144e9c82d', 'IMAGE', 'https://cdn.chotot.com/MjMEDX-Ct68jk2-NzkUIVmVphBK3lNmyNWjWExu5TmI/preset:view/plain/31843409b4ffa58e7e9ced9908bd521f-2991978880361230310.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9d1ae10c-4fc2-4537-a32c-cd438ac3d62a', 'c31398b1-bf7a-449b-9da2-268144e9c82d', 'IMAGE', 'https://cdn.chotot.com/kyQWo29r0hEl-kP0Ul6znj3ECHAW6JY1VTuoi1xihZ0/preset:view/plain/59a37e98996f8ed6ead829ee9a6d59c5-2991978880377197048.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ddd407cc-2cd4-4132-a6ce-d7adf7e8291c', 'c31398b1-bf7a-449b-9da2-268144e9c82d', 'IMAGE', 'https://cdn.chotot.com/SI1tgniGfpWNDDU5tgVT2chVW3Bwsk4hp74t-hvq8DQ/preset:view/plain/95a2f3c9d6a22f0af2eccb7824c8e3aa-2991978880434748569.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9b48abbc-2a09-440d-a920-2cfab461d4ef', 'c31398b1-bf7a-449b-9da2-268144e9c82d', 'IMAGE', 'https://cdn.chotot.com/vXm2vy2UvPh_Y7BVg4RKQIz1l5f6pdcLNjHv1qWwP04/preset:view/plain/464f81775a139406a79ca7544a2c9c8a-2991978880497101252.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a3f74a80-673b-4747-98bd-7758c0f73f29', 'c31398b1-bf7a-449b-9da2-268144e9c82d', 'IMAGE', 'https://cdn.chotot.com/esj1h1WhGsttPf7sdv-rBaGTfqKiiMxeHztCQTimEDY/preset:view/plain/b069de5eba0644e901f9753ade5f9f06-2991978881122679961.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b9c2ce76-bb6b-43e6-b424-c7fa36dbd1ce', 'c31398b1-bf7a-449b-9da2-268144e9c82d', 'IMAGE', 'https://cdn.chotot.com/ktTE96meDrVFWK_pD37O5zeQ33_qziry6fLhU3oHa4E/preset:view/plain/f93d60dd2fcebab276e48b595e297b29-2991978880442159937.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5eac4586-dd86-4bb7-97f4-bb824b01294a', 'c31398b1-bf7a-449b-9da2-268144e9c82d', 'IMAGE', 'https://cdn.chotot.com/8hRDOV4jFBvIaHEIZlpXwEy64WHwEXJoEy7GrHOP3iw/preset:view/plain/46a4bddf9df76cc38e802995f9d7427d-2991978880439828072.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f8672927-8a31-41ed-9b59-13f55fd03f5f', 'c31398b1-bf7a-449b-9da2-268144e9c82d', 'IMAGE', 'https://cdn.chotot.com/z2iCo0qCxuS4Ux-fhowLEpnRmFRmAlfKZyBCw9sKV8A/preset:view/plain/d5e525ec9c8ba7a3e594183d15037ce0-2991978880530897547.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('33baf553-e397-49fe-a7be-4e91fe9415ce', 'P_128791629', 'APARTMENT', 'Phòng studio sang xịn mịn full nội thất ban công', 'Studio rộng rãi thoáng mát 
Full nội thất 
Ban công lớn rộng rãi 
Thuận tiện đi Q1,3,7,9, bthanh
Giờ giấc tự do ra vào vân tay 
Đảm bảo an toàn pccc', 'UNDER_OFFER', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 35, 5500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('82dd9e40-45ce-476a-82cf-551403b470c9', '33baf553-e397-49fe-a7be-4e91fe9415ce', 'IMAGE', 'https://cdn.chotot.com/fFJhK50u8SS2IURfsBQ0MfNCiodIVM1NMqH_UJZop4Y/preset:view/plain/af53ff6b0e91c2fad0d9199b99d04b3b-2956103714533903333.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7d92e404-924c-4c61-aecc-c37a7f9e488a', '33baf553-e397-49fe-a7be-4e91fe9415ce', 'IMAGE', 'https://cdn.chotot.com/mLLVuIsQ5JUyHZ7QVNw8TnuQSRqCueFSsULdClodiMw/preset:view/plain/a065eeb26afbe639831204e2d9958810-2956103714248970112.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('47cad9f5-5401-4cde-a41a-fc19d01b52dc', '33baf553-e397-49fe-a7be-4e91fe9415ce', 'IMAGE', 'https://cdn.chotot.com/RyVUGLOUbVUDc9o-wW-0jorMGiYDFP5dB7zwhitYU9U/preset:view/plain/7f0e33b9d2a954ea56260c0a9cee432e-2956103714065591649.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5ac23f8d-96bc-4a10-9038-ebc18b2af465', '33baf553-e397-49fe-a7be-4e91fe9415ce', 'IMAGE', 'https://cdn.chotot.com/IDgOT0ihxm98QuqIwOf5V7mCDlP-R_tThG_4Pza3eU4/preset:view/plain/15a0d68c7a32935b35b490d72f40caba-2956103714216882179.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('722d5600-2f40-4cd9-bc13-8467df86369d', '33baf553-e397-49fe-a7be-4e91fe9415ce', 'IMAGE', 'https://cdn.chotot.com/wcLF84qx0XsOlRtvgILjwc9jmjKseHoBXekl0klngTU/preset:view/plain/6d05e48f558b1ad051aa171189b699f7-2956103714332341649.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('2af51149-520b-40b2-a9c0-502215a8fccc', 'P_133941164', 'APARTMENT', 'Studio View Thoáng, Ban Công Riêng - Gần Emart, CV Gia Định & Sân Bay', '💥 Địa chỉ: 201 Nguyễn Thái Sơn, P7, Gò Vấp
Giá: 5tr8-6tr5
💢Tận hưởng không gian sống thoáng đãng với ban công riêng, đầy đủ tiện nghi và vị trí cực kỳ thuận tiện.

✨ Ban công riêng đón nắng, đón gió
🛋 Full nội thất, chỉ cần xách vali vào ở
🍳 Bếp và WC riêng, sạch sẽ, riêng tư
📍 Chỉ vài phút đến ĐH Công nghiệp TP.HCM, Emart Gò Vấp, Công viên Gia Định, Sân bay Tân Sơn Nhất, Phạm Văn Đồng, Nguyễn Kiệm – thuận tiện đi học, đi làm và di chuyển về các quận trung tâm.

Phù hợp cho người đi làm, sinh viên hoặc cặp đôi cần một không gian sống tiện nghi.

📩 Inbox ngay để được tư vấn và hẹn xem phòng.

☎️ ***', 'AVAILABLE', 'Quận Gò Vấp, Tp Hồ Chí Minh', 30, 5900000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f9f64e62-4f63-48fd-884f-4bf077186518', '2af51149-520b-40b2-a9c0-502215a8fccc', 'IMAGE', 'https://cdn.chotot.com/JmVgqlTosI0COBe_ouSRC6DmUVyUhiOp8a8dTRhQaII/preset:view/plain/2da744c2f0c69fc424b7629e75664be6-2996123585960125476.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7be0e1c1-13e6-445c-93ff-79f396e35759', '2af51149-520b-40b2-a9c0-502215a8fccc', 'IMAGE', 'https://cdn.chotot.com/QeRWhKlhjVl6KaZL17vMa85O7fCCCoEgJ0GB_0rzSxI/preset:view/plain/48bd144c055e454da49bff221bb08299-2996123586314517229.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('400364d1-c6f0-4522-827f-da0b6aae3fe9', '2af51149-520b-40b2-a9c0-502215a8fccc', 'IMAGE', 'https://cdn.chotot.com/8_AOFGz8FPwFPQeTngjs7_D7qI47HJSwV4XMBlPQ99A/preset:view/plain/b8902c7b3e3e1a946985e4a9b6a2ecaf-2996123586440941159.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('164ee669-a9eb-474c-8285-88349800fcc2', '2af51149-520b-40b2-a9c0-502215a8fccc', 'IMAGE', 'https://cdn.chotot.com/JbniU0ohZMKGdf2pxkObLodUd6DlFNFe0itDVuO3I0Y/preset:view/plain/632c7c9c2eb4c86f147f57a2d3d334ad-2996123587685916760.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('620a3570-aec9-4146-a1a9-75acca5eeab7', '2af51149-520b-40b2-a9c0-502215a8fccc', 'IMAGE', 'https://cdn.chotot.com/kjkNVnMJ9uO7l0ndMuiHZCvrRh8Oqfl-c0d-MiKhST8/preset:view/plain/034c6d773b25d4b903eb3dd1d39177f9-2996123610336538203.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('07583891-3f7a-4163-8233-5a20b2464426', '2af51149-520b-40b2-a9c0-502215a8fccc', 'IMAGE', 'https://cdn.chotot.com/GVz9u-3P56fe1MidpirpW2sjH3ZqynxsViSAEUXD-Ng/preset:view/plain/f8a3dfec1d2f634396bb45e0602a90cb-2996123611358765144.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ae15abea-3ecd-4176-91fd-f0d41acb4eb0', '2af51149-520b-40b2-a9c0-502215a8fccc', 'IMAGE', 'https://cdn.chotot.com/HASMQj6U-XWO6qS7yjrLA3VaKayMoBr9FwI5_q4Na1A/preset:view/plain/5612957008e5c75090a34459fdd643ad-2996123611254539748.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f7ec63a7-d967-4c8a-8590-dd64f0e7b165', '2af51149-520b-40b2-a9c0-502215a8fccc', 'IMAGE', 'https://cdn.chotot.com/yFTwl6N69xK1cuowhsdn4l_g2j_2ippAfKJ4ciTz_U8/preset:view/plain/a4377b6d945a6e5a176f121b0a2cdca5-2996123610567651108.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b5a1e220-253d-42eb-b308-daa3f1b8e0ba', '2af51149-520b-40b2-a9c0-502215a8fccc', 'IMAGE', 'https://cdn.chotot.com/5hVO5eVNlcpFJpwoDYKwbZqaqHfAgUEBtYCBXwHgjHY/preset:view/plain/63a40b03ba32c444eeae0e1cb617471f-2996124389085694329.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e374516a-d230-4d35-906e-133e0a276412', '2af51149-520b-40b2-a9c0-502215a8fccc', 'IMAGE', 'https://cdn.chotot.com/Q9DJTt5-wExM-y2xMjYl1K6S9x9VjexxiVYxpo0kQNY/preset:view/plain/293c907ca46cf97d1e905f1e15df9ba5-2996124389239396505.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5c8b560d-260a-48c2-8624-ea290c7a4c3c', '2af51149-520b-40b2-a9c0-502215a8fccc', 'IMAGE', 'https://cdn.chotot.com/LJPrCsXWrRjUwuUmV7cXmYhA9leqWvg14ZDzIqOZ_oc/preset:view/plain/7a915d9223cb955534bba652d5dc093e-2996124389176093623.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('29898694-602f-4fe6-b138-61a8482b4c9e', 'P_133720261', 'APARTMENT', 'CHDV Ban Công Cao Cấp Giặt Riêng,Gần ĐHSG,Sư Phạm,KHTN,Cầu NVC', 'Dự án: 
Studio 5tr5
Duplex 6tr
Thông tin chi tiết: 💎 Luxury Home - Nơi ở lý tưởng cho tín đồ mê nhà CỰC XINH

Vị trí: Dương Bá Trạc - Quận 8

- Đầy đủ tiện nghi thông minh
- Khu dân cư yên tĩnh, an ninh
- Cửa vân tay,không chung chủ
- Ngay cầu Nguyễn Văn Cừ qua Q5,Q1 2p..
Đại học sài gòn,đại học sư phạm,đại học khoa học tự nhiên,cầu chữ y,phạm thế hiển…
📞 Hotlin.e or Za.lo: gặp Khôi để được tư vấn phòng phù hợp ạ !!', 'SOLD', 'Quận 8, Tp Hồ Chí Minh', 25, 5500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4aaf1344-bb02-4a0c-a924-576781fa2c05', '29898694-602f-4fe6-b138-61a8482b4c9e', 'IMAGE', 'https://cdn.chotot.com/RPlbjaf2hWInYBWiwxpYSxr979NANLN8upy8ShyKe_U/preset:view/plain/668651d7b7f6d859aa5f57c93e96814a-2995086973050320851.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('666df4d0-7205-47ed-8b7e-7e7d15fb252b', '29898694-602f-4fe6-b138-61a8482b4c9e', 'IMAGE', 'https://cdn.chotot.com/h4SYMhXFV2b-IqfzrGguMLZNQJZEBx6UpWBhujHwu7M/preset:view/plain/c403d7bb1f6c1fbeb9c173c022f879c7-2995086974058914944.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('147ca3f7-e326-46a1-ab05-8f5c1504450d', '29898694-602f-4fe6-b138-61a8482b4c9e', 'IMAGE', 'https://cdn.chotot.com/Di_V5-G_Dosfc2n6WooTtPToYtrX_pbjwj9B9NrbpEc/preset:view/plain/81a8896c69a00547003f818fe856dcc1-2995086974151086960.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('105481b4-9f67-48ff-806c-71e985c0fbc4', '29898694-602f-4fe6-b138-61a8482b4c9e', 'IMAGE', 'https://cdn.chotot.com/nAjIciTMGCubOm5QRxEBtVqsS7arH89WR1b2DY1ERUU/preset:view/plain/d4d41ad1f58a6e95f5092e722775dec6-2995086974184450305.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b95b452f-acea-4c77-9f01-bf0314c2bc75', '29898694-602f-4fe6-b138-61a8482b4c9e', 'IMAGE', 'https://cdn.chotot.com/qssTphVNSwtqCVHc_JI1VCOeZ5NSRnOLDfvnNwEyuB0/preset:view/plain/05dc6a37eb13c4533fd3b89d60681419-2995086974277615611.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('668c9e16-9d54-49c6-b9a0-e66f3cf260ea', '29898694-602f-4fe6-b138-61a8482b4c9e', 'IMAGE', 'https://cdn.chotot.com/WvdiDOxBVOtDd8b7Ye2Rt-Vn8T_sTQKdl6wOxcRIGEU/preset:view/plain/91f3f9b935745a7bf75cdc0d2d648445-2995086974571145205.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('69ca6822-559a-4d52-a4d3-975bb50a3012', '29898694-602f-4fe6-b138-61a8482b4c9e', 'IMAGE', 'https://cdn.chotot.com/SBwtPcM0sdu4p-DQYdTZhzH3H5J27UXo5CbttJ7qqt4/preset:view/plain/f7a4a9c6e739025272e59ad8cc84974e-2995086974406706020.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5641c789-f50d-4fe8-b895-8667b966189d', '29898694-602f-4fe6-b138-61a8482b4c9e', 'IMAGE', 'https://cdn.chotot.com/0P_dS78OuXbYXpZE_y4ZIh8pWwWaOHxqqfTisoweTG0/preset:view/plain/e623d4f866300962e6c265245be3bca7-2995086974461384485.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('e2e4c6ef-7972-4fa8-a153-fdebb7bdc5be', 'P_133941147', 'APARTMENT', '🏡 CHO THUÊ CĂN HỘ CHUNG CƯ MỸ AN – SAU LƯNG GIGAMALL, THỦ ĐỨC', '🏡 CHO THUÊ CĂN HỘ CHUNG CƯ MỸ AN – SAU LƯNG GIGAMALL, THỦ ĐỨC
📍 Vị trí: thuận tiện di chuyển đến Phạm Văn Đồng, Bình Thạnh, Gò Vấp và trung tâm TP.HCM.
📐 Diện tích: 73m² 
🏠 Tầng 13, 2 phòng ngủ – 2 WC , view thoáng mát
Full nội thất như hình, vào ở ngay
💰 Giá thuê: 10 triệu/tháng
📄 Hợp đồng thuê: Từ 1 năm trở lên.
📞 Liên hệ Hotline/Zalo: *** Em Thảo để thuê nhà', 'UNDER_OFFER', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 73, 10000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('64cd067d-08ba-43ca-ad2d-7fd86a6f715e', 'e2e4c6ef-7972-4fa8-a153-fdebb7bdc5be', 'IMAGE', 'https://cdn.chotot.com/tB_pPkijnPiJ_6oLipnk6DpWzn7Gd_HZxxxV2xc77RE/preset:view/plain/17f85bd2bcae624cb5d41aaae805cf44-2996124314479073433.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bf6d8f46-2e72-4988-aab9-51c6b364de9a', 'e2e4c6ef-7972-4fa8-a153-fdebb7bdc5be', 'IMAGE', 'https://cdn.chotot.com/liOTaD4qfbUn3Iiq1Fm5Mp0Vy8hzWkDyWp-i56Zr6bg/preset:view/plain/f456b2ef9f38bfd32a32f20519a281b1-2996124314689181777.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d7d5bc9f-3670-4750-a4d0-b91bfb71acb1', 'e2e4c6ef-7972-4fa8-a153-fdebb7bdc5be', 'IMAGE', 'https://cdn.chotot.com/bm9yid9QdlAiJelBhqH_-2cL98c9cHrYdlxWhknQ42w/preset:view/plain/69f71067ae6424ba333cf06f036afb4d-2996124314597368868.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('46ce392e-b139-4678-9b7f-af928fd89d5b', 'e2e4c6ef-7972-4fa8-a153-fdebb7bdc5be', 'IMAGE', 'https://cdn.chotot.com/KPZvMHJBC67hsK6XpzFLPvkSOMQDOaesbyidcwuePc0/preset:view/plain/fc764965f7dc2991cf6922ee08fd91d5-2996124314598884836.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c90f75cd-59d7-4207-8852-7da332f1397e', 'e2e4c6ef-7972-4fa8-a153-fdebb7bdc5be', 'IMAGE', 'https://cdn.chotot.com/gZsFEHL2SCDMgMJKTeuDHsQ_1IkbCAU9ZUUYbq9_M7s/preset:view/plain/df16495672b27350ec126175f13447d6-2996124314590958591.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('012de25c-2179-44a2-a04a-89d9f63d1e30', 'e2e4c6ef-7972-4fa8-a153-fdebb7bdc5be', 'IMAGE', 'https://cdn.chotot.com/UOodDG2lQXKiiu-ADOoyZrZ1efA5C_ZqP1yMBkzebL4/preset:view/plain/2b2f148a2a38a484188fed062601f5ee-2996124314596089944.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('26793fd5-c80e-49bc-8501-3d4a81bb4cb8', 'P_133304586', 'APARTMENT', '❤️ BÁN CĂN HỘ CHUNG CƯ TÂN BÌNH APARTMENT 70m 2PN2WC– 32 HOÀNG BẬT ĐẠT', '❤️ BÁN CĂN HỘ CHUNG CƯ TÂN BÌNH APARTMENT – 32 HOÀNG BẬT ĐẠT, P15, Q.TÂN BÌNH

📐 Diện tích: 70m²
🛏️ Thiết kế: 2PN – 2WC
💰 Giá bán: 2,5 tỷ

✅ Vị trí đẹp, gần chợ Tân Trụ, Etown, sân bay Tân Sơn Nhất
✅ Khu dân cư an ninh, thuận tiện di chuyển Phạm Văn Bạch – Trường Chinh
✅ Phù hợp ở gia đình hoặc đầu tư cho thuê

☎️ Liên hệ:  Trần Toàn
🤝', 'AVAILABLE', 'Quận Tân Bình, Tp Hồ Chí Minh', 70, 2500000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e0cc4e10-a015-4df0-a417-f0173e082e55', '26793fd5-c80e-49bc-8501-3d4a81bb4cb8', 'IMAGE', 'https://cdn.chotot.com/NDWxmE0JQhOLiHtM4-vbrCtQ1-YXlkFbLaohMsryXo8/preset:view/plain/40323f27f0b13e3c89e465fbd20fc9b6-2992979431918878775.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2f338804-9342-46a8-ba9c-065d8e666f3d', '26793fd5-c80e-49bc-8501-3d4a81bb4cb8', 'IMAGE', 'https://cdn.chotot.com/J6_hbjtNn7ga35gfqDoE8BC0Zc01QKEExAL1UKFRdf4/preset:view/plain/2a9966624e6288b6be06aafc91f1508c-2992979432071689741.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d2222509-96ac-4851-9287-4bfc0973d5b4', '26793fd5-c80e-49bc-8501-3d4a81bb4cb8', 'IMAGE', 'https://cdn.chotot.com/Rrbg4v7xUO44VOCpqicq8oD0YwGxtM4f0xifWiJaX2o/preset:view/plain/35286fa4985154de034adea5e500359e-2992979432117070111.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('998391ca-efbf-4d5a-bbb5-e498f3c6bb15', '26793fd5-c80e-49bc-8501-3d4a81bb4cb8', 'IMAGE', 'https://cdn.chotot.com/79OrKLBgSSmUulwYW7V_lfhXfK5ni03idbbdOVyrlx8/preset:view/plain/e5372714e9f9c5ef388710f911ce520d-2992979432115116017.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b6cf0bd1-ed35-4361-999a-260556a4dc01', '26793fd5-c80e-49bc-8501-3d4a81bb4cb8', 'IMAGE', 'https://cdn.chotot.com/KUbo1YlZQSmY-xZmQdWKnJvTSiwFWGapGsJMUkEZGW4/preset:view/plain/440f3d3503935b0c715b92a2e3c8d228-2992979432925577271.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('321246e8-b7fb-45a8-8667-d2d4ce02103c', '26793fd5-c80e-49bc-8501-3d4a81bb4cb8', 'IMAGE', 'https://cdn.chotot.com/ZAdcrRuIaHUxO0_-yaFbN435Dv_b8F9qn0oyDYQK_WU/preset:view/plain/0fbe1936d0d39453a8114300b23c060f-2992979433346823693.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bd3facd6-0d0f-4c75-88ef-fc6a73ddff75', '26793fd5-c80e-49bc-8501-3d4a81bb4cb8', 'IMAGE', 'https://cdn.chotot.com/2LTO4zo7jZkjS3RWziMyKpuqY0SmEpA1O2YhLuRhQWQ/preset:view/plain/1ff3fe91225f877b236ad867ce46cf99-2992979433692239857.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('9793c5a8-4b41-4a22-b5c9-bb60e2b8d931', 'P_133808782', 'APARTMENT', 'Trống Sẵn 1PN Mater Full NT Ở Vinhomes Quận 9', '
👉 Dành cho nam, nữ, couple,…
✨ tài chính dao động 2tr5-4tr5 
📍Thuận tiện qua: Khu Công Nghệ Cao Thủ Đức, Ngã Tư Thủ Đức, Nguyễn Xiền, Nguyễn Văn Tăng, Lê Văn Việt,...
Tiện ích:
-   Khu vực an ninh tốt, PCCC đảm bảo.
-   Nội khu có công viên, hồ bơi, khu vui chơi thể thao ngoài trời, quán ăn, Siêu Thị Vincom,....
-   Gần bệnh viện, trường học,...
-   Điện: 3k5/kwh
-   Nước: 80k/người
-   Phí dịch vụ: 150k/người

☎️ Liên hệ 24/7:096279837 (  Tiến ) ', 'SOLD', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 30, 3500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fb2db7f7-19a0-497e-bce0-49d817914c18', '9793c5a8-4b41-4a22-b5c9-bb60e2b8d931', 'IMAGE', 'https://cdn.chotot.com/o7tyjpnVXR_82z7RGdb9t1XOSUDrVR5hJxvry28uavQ/preset:view/plain/f4acb372f63bc069d7e972ee5ba6ea60-2995115665955701604.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('960b6a78-0871-4bbe-9a3c-a798ca5e1dea', '9793c5a8-4b41-4a22-b5c9-bb60e2b8d931', 'IMAGE', 'https://cdn.chotot.com/qo-jgBnMaPAmYYtMdorzwMIif-7HtdI9T--q-Lg40i8/preset:view/plain/5f82fd7cd3149e537698d2157c11ce35-2995115665655195905.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('99cc0336-bd77-40b5-be94-972b3acc1ff4', '9793c5a8-4b41-4a22-b5c9-bb60e2b8d931', 'IMAGE', 'https://cdn.chotot.com/eTk1Icfr1-kZGbqQy_F6OA9EwdBLL_2cqnh--UTZZt0/preset:view/plain/f216f828a8d8a339732505084f282115-2995115666806865810.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ded914de-4f4d-4155-9552-799db3438a46', '9793c5a8-4b41-4a22-b5c9-bb60e2b8d931', 'IMAGE', 'https://cdn.chotot.com/t-VlLMvyXDnZ6IhZdBFznCsv0YVTxqqswWM0EZGpYVI/preset:view/plain/3d6c940e1f1d631bc361342b5f3c2735-2995115667118258131.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d11695df-749c-4ee2-bb1d-1cd6a1a98a86', '9793c5a8-4b41-4a22-b5c9-bb60e2b8d931', 'IMAGE', 'https://cdn.chotot.com/uTNweYPIuEXkGAsN34Zywr3rDPF3YVrGI1xFYzd5dDc/preset:view/plain/4ff10d51985d32a82fdd5c89e60f7a77-2995115668074942261.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6c4aa236-248f-4bbc-bd72-576353ce83b8', '9793c5a8-4b41-4a22-b5c9-bb60e2b8d931', 'IMAGE', 'https://cdn.chotot.com/kUeT9drMEypYdX06tQlTj4oTx13typpiKPn6EfTLf-8/preset:view/plain/cde691bb01f78b35d688e97fdd818728-2995115668333646704.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('75d3e680-167c-4525-a6c6-12e75efd3855', '9793c5a8-4b41-4a22-b5c9-bb60e2b8d931', 'IMAGE', 'https://cdn.chotot.com/iOJkLmXsjZmHdiqx_mKzFRe2Km45D64bd2bQnofBG_I/preset:view/plain/917c3c7c968b90ed5647aed0cadffd35-2995115669239681904.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a7e6124e-6f55-4d1c-a969-b70d8442a53c', '9793c5a8-4b41-4a22-b5c9-bb60e2b8d931', 'IMAGE', 'https://cdn.chotot.com/PbTj1aAKKzPDW7D8viRBIcFMSVz2RHNRl8uKpnCrpeA/preset:view/plain/8cf08a9e590be087a87f140e3efb42b5-2995115669462205284.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3d7e1557-95d6-4f09-ba22-180b2a788676', '9793c5a8-4b41-4a22-b5c9-bb60e2b8d931', 'IMAGE', 'https://cdn.chotot.com/g17CGfC8Z04OfuMLieNTku4dfIt2JlIS4KnwA7CgUGA/preset:view/plain/59dd1f07ced68065ea7e3605e7f7ee36-2995115670460913092.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9ee15265-bdc6-4b46-9735-93623b9bc44d', '9793c5a8-4b41-4a22-b5c9-bb60e2b8d931', 'IMAGE', 'https://cdn.chotot.com/c4BrxcHz0aZZxDUiYVxjJa17U8h6KXO5Z2p9oOd76ZA/preset:view/plain/bd7ba96468fea28a6d91b02e9e20e395-2995115670708778963.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('b5c1ef7f-497d-4351-9484-69ef7c96d474', 'P_133616722', 'APARTMENT', 'Cho thuê căn hộ Cityland 2pn 2wc giá rẻ chỉ từ 13tr/ tháng', 'CHO THUÊ CĂN HỘ CITYLAND PARK HILLS – GIÁ TỐT.
 Căn hộ 2PN – 2WC, không gian rộng rãi, phù hợp gia đình hoặc người đi làm.
Giá thuê cực hấp dẫn:
 có nội thất: chỉ từ 13 triệu/tháng
 Khu căn hộ an ninh, nhiều tiện ích: hồ bơi, phòng gym, công viên, siêu thị, trường học... Vị trí thuận tiện, môi trường sống văn minh.
📞 Liên hệ ngay  sdt  để xem nhà thực tế và nhận giá ***!', 'AVAILABLE', 'Quận Gò Vấp, Tp Hồ Chí Minh', 76, 13000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3165a59b-1f2f-41b2-be93-654ae8633112', 'b5c1ef7f-497d-4351-9484-69ef7c96d474', 'IMAGE', 'https://cdn.chotot.com/QVrNRXHMQ2cXV_uVHLU-IVj26wQg5zfzhCgimlVGKL4/preset:view/plain/992162a799cc2d5c14fc5613be5676ca-2993645492645927751.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('69198140-8d79-4e77-9c82-7f3e9ee26a3d', 'b5c1ef7f-497d-4351-9484-69ef7c96d474', 'IMAGE', 'https://cdn.chotot.com/GGSZvUIsSG5_eh4JDMFUBkd6ak5uASz8Szaked1fN-U/preset:view/plain/426c4dc9ca7383775f5083ddd55e6214-2996120893790000424.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('01cfee70-594f-4a30-ba14-4c9ff6b648ac', 'b5c1ef7f-497d-4351-9484-69ef7c96d474', 'IMAGE', 'https://cdn.chotot.com/P84Sv5AS6LWK8JWFdU9wkqWFycYbQNzqUCrUwx_Lqh0/preset:view/plain/57faefc61904e7ab8d736bd653cd1884-2996120893779426029.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8e92e7e7-32fc-4569-833e-ca89f14a5bf5', 'b5c1ef7f-497d-4351-9484-69ef7c96d474', 'IMAGE', 'https://cdn.chotot.com/Nuv2TMYYqQKHJC2K-6gUqc-6rxbEcfSz0WSYzbDeLhg/preset:view/plain/bc0f90ccb6ecc40add631fdb20a245bf-2996120894970673901.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('7942935c-a498-4522-b640-9f230e21f477', 'P_132923476', 'APARTMENT', 'Phòng Sinh viên Sát Đại Học TDTu đi Bộ Chỉ 3 phút', 'Dự án: 
Thông tin chi tiết: SIÊU RỘNG FULL NỘI THẤT NEW 100%
Phòng rộng thoáng mát phù hợp ở 4 người
Có đón gió lấy sáng
Thuận tiện qua Q4, Q1, Q8
Có khu giặt phơi chung', 'SOLD', 'Quận 7, Tp Hồ Chí Minh', 35, 3600000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3270f99f-9142-407e-be7a-cad4dcc57e3c', '7942935c-a498-4522-b640-9f230e21f477', 'IMAGE', 'https://cdn.chotot.com/MGhqDiTm-9vjvWuUotoGARAAepcruKgnpccGdH3LOAk/preset:view/plain/37d172a718d0020a622ed4ed6772ffa9-2988314560703108235.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('afc135df-a225-4eee-8a2d-d2e00fbe543c', '7942935c-a498-4522-b640-9f230e21f477', 'IMAGE', 'https://cdn.chotot.com/p0EeNBi_OjmpybflBfHoHwWzmXA1jKqaFlZffvPxmH8/preset:view/plain/ee60b0207e73c216a56931198e1b4ff8-2988314560863486653.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ae57848c-b63c-4142-9c86-edf8272d13da', '7942935c-a498-4522-b640-9f230e21f477', 'IMAGE', 'https://cdn.chotot.com/B8XVfPXn6PU4_X-13-ilcNNWZZOnX0bp6lIXgeo0Jv0/preset:view/plain/288b28f3ab9cbacbf95d73c417cc7231-2988314561008544140.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e105cae8-8288-4b40-85cf-14f90fd5660c', '7942935c-a498-4522-b640-9f230e21f477', 'IMAGE', 'https://cdn.chotot.com/-XqDhwQCEi9HjRgkg2EH3eHKOfzDYP3Jdgov9a1_xmo/preset:view/plain/e2e7a94b9390621feeb1559aa0b5fb8b-2988314561215183065.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('1fad41d8-c8eb-4462-b213-7a219a46847c', 'P_132939339', 'APARTMENT', 'CĂN HỘ SÂN VƯỜN, TRẦN CAO 4M - CĂN 2PN VÀ 3PN. CÓ TRẢ GÓP 0% LÃI SUẤT', '- TPHCM đang đi theo Nhật Bản xây dựng Ga Metro dãn dân và người dân đi làm trung tâm TPHCM bằng Metro. Hiện nay Metro số 1 (Bến Thành - Suối Tiên - Sân Bay Long Thành). Metro số 2 (Bến Thành - Tao Đàn - Tham Lương - An Sương). Metro ngay căn hộ Bcons là (Tao Đàn - Hiệp Bình - Thủ Dầu Một). và Metro Bến Thành - Cần Giờ.... Hiện tất cả các tuyến trên đã được thông qua theo cơ chế đặc biệt (Tư Nhân làm)

- Căn hộ Newsky nếu từ ngã tư Hàng Xanh về tới dự án là 12km. Có Ga Metro ngay cửa chung cư
- Căn hộ Bcons newsky gần ngã ba cầu Phú Long (về Q12), chỗ nước ngọt Number One, Cách ngã tư Bình Phước - Thủ Đức 3km. Gần bênh viện quốc tế Hạnh Phúc

- Hiện em đang có 2 căn hộ "sân vườn" ở tầng 3. chủ đầu tư bán nhà, còn diện tích sân vườn là "khuyến mãi" cho khách hàng.
- Căn 2PN - 56m2 - có sân vườn 3m2. View nhìn công viên 6.000m2 (đài phun nước, sân bóng rổ, khu cây xanh...).
Giá: 2,8 tỷ - Ký HĐ 5% và các đợt tiếp theo cứ 2 tháng đóng 5%.

- Căn 3PN - 78m2 - Căn Góc cả 3PN đều có cửa sổ lấy ánh sáng tự nhiên. Có sân vườn 3m2. View nhìn công viên 6.000m2 (đài phun nước, sân bóng rổ, khu cây xanh...).
- Giá: 3,6 tỷ

- Căn Shop-house (tầng trệt) vừa ở vừa kinh doanh. Từ 104m2 đến 150m2. Giá 5,8 tỷ

- Những căn sân vườn này chiều cao 4m. (các căn hộ khác chỉ cao 3,1m). Có lối riêng đi ra khu hồ bơi, gym và công viên.

- liên hệ zalo hoặc gọi trực tiếp *** (làm việc 24/24) đừng nhắn trên web bị trôi tin không thấy được', 'SOLD', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 56, 2800000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5601e911-5234-4933-bbc9-e397e54c887e', '1fad41d8-c8eb-4462-b213-7a219a46847c', 'IMAGE', 'https://cdn.chotot.com/85ueukk--uKcn7K4MRAqEt4Ylb8BKY6GPZ26IhTsWfo/preset:view/plain/d9b2ab33974c323191194c50507a447d-2988445513654774156.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8c9a8357-094f-4ce5-ad8b-53701ad73c00', '1fad41d8-c8eb-4462-b213-7a219a46847c', 'IMAGE', 'https://cdn.chotot.com/Gsyq120jAAmlv8HQC0OpRtDotTtMikJCHsWWfRb_5Ac/preset:view/plain/d45dbe78a252397913898876e1c99c04-2988445515148011916.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('376eeb52-5e7a-4b32-8a1c-a7f36dcddf21', '1fad41d8-c8eb-4462-b213-7a219a46847c', 'IMAGE', 'https://cdn.chotot.com/jfHZQQjSnqPNGivdMiw3JpqmHCIKAnoMJ_aa6OzvCAY/preset:view/plain/7b1bd8529675b5f68422cf5075a1fc93-2988445516890276933.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6275a394-1291-47e8-923c-a1a80bf30a40', '1fad41d8-c8eb-4462-b213-7a219a46847c', 'IMAGE', 'https://cdn.chotot.com/tWhp5SaVzAVvrbb6b3C6g_9l3ohpH2GPb_i_9uJIxgg/preset:view/plain/97a43e87850f30960d4f28f4402b0ee8-2988445517090651845.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f98afc05-69a2-4c0c-a228-6f0dea704a9d', '1fad41d8-c8eb-4462-b213-7a219a46847c', 'IMAGE', 'https://cdn.chotot.com/_EoG1NB0j98GC6nqVTd9osW7S_SuWlyaN8U_1ZqQjMQ/preset:view/plain/0f51e20d7d3a8525b24f9df9f3659af6-2988445517306292755.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c503e09b-e09e-4cdc-a22f-9d9b54ee5927', '1fad41d8-c8eb-4462-b213-7a219a46847c', 'IMAGE', 'https://cdn.chotot.com/vJj-Z3gfv2r3kv7IGPsb_NtyoqD-4gIA6DdxTzYx7wk/preset:view/plain/66d742cfaec4fa44b6496287012355d6-2988445516070824332.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0e8c4bb8-74c2-4995-8e93-942fb098276b', '1fad41d8-c8eb-4462-b213-7a219a46847c', 'IMAGE', 'https://cdn.chotot.com/0yp-N-4aC6n2xtQuAKMTc2xy162XLYMFKkeeQMoT33M/preset:view/plain/e149bcd95d9da8cb8b89ed2c95cb1b21-2988445514775330501.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('35ac1b9f-17b3-4385-8e9d-da59f7316830', '1fad41d8-c8eb-4462-b213-7a219a46847c', 'IMAGE', 'https://cdn.chotot.com/SqmMlKqU8RR3__sUdMYUiImNy7GU0h_Ki4r17n0ZpaA/preset:view/plain/d21738f7e0abf43b420542e4f0ffddce-2988445515960637883.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1b4ebe5b-37a8-40bc-9c1b-f77696c30dbe', '1fad41d8-c8eb-4462-b213-7a219a46847c', 'IMAGE', 'https://cdn.chotot.com/dGvaFf34v31G1gbEr212soVBTe9X5Ca2QCA0_gCXrOs/preset:view/plain/dd2e197cc3363f75d6c0c98f580c6e34-2988445514249296315.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('2625f0a7-ba53-4f4a-9022-b6ae5699e262', 'P_133941081', 'APARTMENT', 'Phòng Mới Xây Ngay sát Lotte mart Quận 7 cho ở 4 bạn', 'Dự án: 
Thông tin chi tiết: DUPLEX  SIÊU RỘNG  100% 


Phòng rộng thoáng mát phù hợp ở 4 người
Có đón gió lấy sáng
Thuận tiện qua Q4, Q1, Q8
Có khu giặt phơi chung', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 35, 5500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('52dde7b5-0531-44b3-ae49-536b8873bf8c', '2625f0a7-ba53-4f4a-9022-b6ae5699e262', 'IMAGE', 'https://cdn.chotot.com/QlSsNx6pLHIQwU2fugcuIlPVINCjQk_W7mRwrlFDBV0/preset:view/plain/a0340d6045df9ca8e88dafc23a67cc43-2996123969933560185.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('646ba92b-f55d-41ed-a498-46ccf787cd42', '2625f0a7-ba53-4f4a-9022-b6ae5699e262', 'IMAGE', 'https://cdn.chotot.com/iWGqSLz17UVdUqKQ3R5vi6MlX6T0SkaNi5_CqvyN0bA/preset:view/plain/0723a773b961cc6ab5d00d2d71bdfdca-2996123969471598183.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c241663c-0c0c-4cc1-ac0d-108f7ad4886c', '2625f0a7-ba53-4f4a-9022-b6ae5699e262', 'IMAGE', 'https://cdn.chotot.com/miqDJaL9HInYZ-h-nglSU1qnBHVyGXDSrgfF8da9fDc/preset:view/plain/2daa6523489e0acf302ef6e328bee734-2996123970277256119.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1443cc1d-6486-4e77-ae1a-85a937708d65', '2625f0a7-ba53-4f4a-9022-b6ae5699e262', 'IMAGE', 'https://cdn.chotot.com/jLQD68qeOAnUeWrSfczEkaEoRLkU8bibyY26mTwXFcM/preset:view/plain/9a81a21fb392187a4f13f2e165d4005f-2996123970321159464.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('eabbea4a-cdb2-485d-a892-6eeccfc5d28c', '2625f0a7-ba53-4f4a-9022-b6ae5699e262', 'IMAGE', 'https://cdn.chotot.com/TJpkt_6i3a-6z8ldeKIPIHbR1An6ecwt-gE2Eg56n-s/preset:view/plain/e09e7a0d091953e93337489ff60e1eb4-2996123970459113625.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('76675233-9ab1-41ae-8d38-72d57a737bf9', '2625f0a7-ba53-4f4a-9022-b6ae5699e262', 'IMAGE', 'https://cdn.chotot.com/AIDjldALbNxfBIfGI1dSEqhPoAeJT0_Gnq7HB8utkAI/preset:view/plain/b2b631f27fe9da8e3e47aad9099e7d7a-2996123970477213156.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5469bd49-8762-4a73-9d32-45c2e454e762', '2625f0a7-ba53-4f4a-9022-b6ae5699e262', 'IMAGE', 'https://cdn.chotot.com/oPD5bTHbwYjNn8t0jTS9j-cyrHh31-HTLSHPJY12GKs/preset:view/plain/c4d13c9d694a29b8741c7c819d038347-2996123970594742360.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('eaadf49a-d4cc-49ab-aa38-09a55506465c', '2625f0a7-ba53-4f4a-9022-b6ae5699e262', 'IMAGE', 'https://cdn.chotot.com/I1zgG0QoNtCd1c2zDVW4JGSo7qRNN8d0TdfJt_A3flg/preset:view/plain/e2e7b48c68d731de05082df6e2234bac-2996123971193590783.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d35dadaf-a1ee-48e6-990b-20dc438f26bb', '2625f0a7-ba53-4f4a-9022-b6ae5699e262', 'IMAGE', 'https://cdn.chotot.com/ccg2jOF1B81SDf2oPNV30hdQ7QGTFKNxu_aBAXMH2fY/preset:view/plain/60a58e377e3ffdf1102f778172eded44-2996123970829758043.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('966aac53-8cb0-42a9-b26d-1a0bdc1dc7b0', 'P_133423311', 'APARTMENT', 'Hot căn siêu phẩm 3PN 2WC tòa Garden Gate chỉ 18tr5 gần cv Gia Định', '💥 GIÁ TỐT – CĂN HỘ RỘNG – GẦN SÂN BAY 💥
🏙 CHO THUÊ CĂN HỘ GARDEN GATE  🏙
📍 08 Hoàng Minh Giám, P Đức Nhuận – Gần Công viên Gia Định & Sân bay Tân Sơn Nhất
🏠 90m² – 3PN – 2WC – Full nội thất xịn
💰 18.5 tr /tháng 
🎁 Tiện ích miễn phí: Hồ bơi, gym, BBQ, bảo vệ 24/7
📞 Zalo/Call: (Trình) – Xem nhà trực tiếp

#TheBotanica #CanHoGanSanBay #ChoThueCanHo #CanHoTanBinh #CanHoNovaland #BotanicaPremier #OrchardGarden #GardenGate', 'UNDER_OFFER', 'Quận Phú Nhuận, Tp Hồ Chí Minh', 90, 18500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('aebbb845-5469-433a-a08b-8753647362f5', '966aac53-8cb0-42a9-b26d-1a0bdc1dc7b0', 'IMAGE', 'https://cdn.chotot.com/d8yPA7RkHn0R3QL5sfn6uKy5NPdNm-hQnCXiVGE9Q0w/preset:view/plain/6d36ca84a3b08fcff0ad854298915dfa-2992183263562514487.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cf8b5d46-3f5e-4826-9d08-2c27f8e88a6a', '966aac53-8cb0-42a9-b26d-1a0bdc1dc7b0', 'IMAGE', 'https://cdn.chotot.com/kaKwpmgB-0UM5O34g9sbAQQyG4S4eTVhPZTJp4X3nJ0/preset:view/plain/36fa029f3967046996287d4f513a3339-2992183263600075652.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('11d586d5-fb71-469e-aefc-1dc2bb4cb6bf', '966aac53-8cb0-42a9-b26d-1a0bdc1dc7b0', 'IMAGE', 'https://cdn.chotot.com/lpODTMrGPa7ZVuvl5cgtYcsjv263GJnBbimFcDFa61U/preset:view/plain/a37f995c3b7c204486d8dcd02f9bec63-2992183263307355241.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('503fc462-8c03-4121-9a11-a874eff5b417', '966aac53-8cb0-42a9-b26d-1a0bdc1dc7b0', 'IMAGE', 'https://cdn.chotot.com/2pn89JDEovGiiDuvMlEMNBhQJBmU1B-X0aGWhB0vjaI/preset:view/plain/cc9a542b0017d1277fff7deeb39a144b-2992183263294062222.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6a97eaf3-2192-4937-9707-1eae9917abb0', '966aac53-8cb0-42a9-b26d-1a0bdc1dc7b0', 'IMAGE', 'https://cdn.chotot.com/GayrQbEkpLu5kmNQLDR31cPPQO1co2NX5TFCTs6uTdY/preset:view/plain/fe1a8e97599bec481cad64d998796449-2992183263588924629.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ee710ecf-adb6-42d0-b8e0-59319f615ea8', '966aac53-8cb0-42a9-b26d-1a0bdc1dc7b0', 'IMAGE', 'https://cdn.chotot.com/EOsrd4ljJ6yKva-Cw9Ejba6ZydodUBahRILAHqf4kJI/preset:view/plain/ad9d98d0fc668f805df83e4d632a9138-2992183263556143822.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a808df37-60ab-4d09-8d0a-6d1769dcd155', '966aac53-8cb0-42a9-b26d-1a0bdc1dc7b0', 'IMAGE', 'https://cdn.chotot.com/sJMfjx7zR_H_k6oCpAlMgukSP3RJEOIgcgJ98vDhXwA/preset:view/plain/e638542d811125e32bea82474ee2aa9a-2992183263430103154.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('92ea2dd2-f8ad-4c92-b5e4-97af53e86662', '966aac53-8cb0-42a9-b26d-1a0bdc1dc7b0', 'IMAGE', 'https://cdn.chotot.com/XSFYye-BV9y1VqeQFrefjDOrlTAtEea9Xbk7E9sMHZ4/preset:view/plain/64c2f587a4c3e4d3b26fa04450fdfa78-2992183516559129813.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('183a3b8f-4621-48e6-af99-0edb516d826e', '966aac53-8cb0-42a9-b26d-1a0bdc1dc7b0', 'IMAGE', 'https://cdn.chotot.com/zzv6j3GAFxLgE0oGjIdv-Nz_2G3HGGJqoxNjDLcLpj4/preset:view/plain/a86c7936cf9ca0dd4fa0a77d50540561-2992183516532260919.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5f6079b2-e1c9-4a94-ad68-b38d0630bd78', '966aac53-8cb0-42a9-b26d-1a0bdc1dc7b0', 'IMAGE', 'https://cdn.chotot.com/r_3aHUBq67mFWs0ZGP-6l9P4FO88iguJpxozQJrmV-g/preset:view/plain/a9f5f97dacb4885b1dede9c06d2aa05d-2992183516630733929.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('5d9bf876-f0a7-48b1-ad09-c38dc64b2378', 'P_133941063', 'APARTMENT', 'Cho thuê căn hộ Akari City 2 Phòng Ngủ 1 Nhà Vệ Sinh mới đẹp', 'Dự án: 
Thông tin chi tiết: Cho thuê căn hộ Akari City 2 Phòng Ngủ 1 Nhà Vệ Sinh mới đẹp
Cho thuê căn hộ Akari City 
2 Phòng Ngủ 1 Nhà Vệ Sinh 
diện tích 61m2 
Giai đoạn 2 còn được miễn phí quản lý 
nhà có ban công 
nhà nội thất cơ bản có rèm giàn phơi
-Akari City nằm tại 77 đại lộ Võ Văn Kiệt, phường An Lạc, quận Bình Tân, TP.HCM -Dự án có nhiều tiện ích nội khu như hồ bơi, gym, siêu thị, nhà hàng, café, khu vui chơi trẻ em, mảng xanh và không gian sinh hoạt cộng đồng.  -Phí quản lý: 13.500 đồng/m² với Giai đoạn 1 , Giai đoạn 2 đang miễn phí -Phí gửi xe có bảng riêng theo từng loại xe và thời điểm.  -Điện nước cư dân thanh toán theo thực tế sử dụng.', 'UNDER_OFFER', 'Quận Bình Tân, Tp Hồ Chí Minh', 61, 8500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c6d71d70-ff60-44b4-aa25-1e66368498f7', '5d9bf876-f0a7-48b1-ad09-c38dc64b2378', 'IMAGE', 'https://cdn.chotot.com/z7EFnFopEB6wlMnWZ8J_dBLaCsPL61GpiEChnJm58wo/preset:view/plain/2882a0e1703a864a37b62552bc7d7e66-2996123864528890807.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b1024180-9bf5-4c2c-9a98-97dfe44adc40', '5d9bf876-f0a7-48b1-ad09-c38dc64b2378', 'IMAGE', 'https://cdn.chotot.com/4M_gn8cRf6RyGbUFb0fGWG_hTB-MPRzN5HNuSHPAajc/preset:view/plain/7dce174cb4d58be40c1e9bd36ad4b2cf-2996123864503437689.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6f8dca0b-cebd-470f-878c-6a25a2ab55c5', '5d9bf876-f0a7-48b1-ad09-c38dc64b2378', 'IMAGE', 'https://cdn.chotot.com/3WWvHkdBQ3ogP1i7TFNo569Zzd6TRMmPerYY9So7x-s/preset:view/plain/bcef94eb42c8dda11e84ecebd8de3111-2996123864494360036.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('282136b4-5d40-422a-88c9-db1da2c6ff97', '5d9bf876-f0a7-48b1-ad09-c38dc64b2378', 'IMAGE', 'https://cdn.chotot.com/Tei9qZbauVliUdHIOKXVe8SzRCKGkxTp1bJOxfQSQl0/preset:view/plain/452596de50d96d9d5b1421801ee404d3-2996123864576989337.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0b5409e2-6a20-48a5-b892-5de4ab9ec884', '5d9bf876-f0a7-48b1-ad09-c38dc64b2378', 'IMAGE', 'https://cdn.chotot.com/4_3kq6FfdQ5SdumnoRFA8x-SshIlzxj3tbhUw4gA5pY/preset:view/plain/b90bd7c5b43d8fbe636a5cbb0479d0c8-2996123864645783143.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('47b1f847-7c97-4327-8443-a7d289941327', '5d9bf876-f0a7-48b1-ad09-c38dc64b2378', 'IMAGE', 'https://cdn.chotot.com/YhJZoIFRVjGAJsg9Ah7efGEPhD8QdRj9sSFuz7SpbSU/preset:view/plain/29eca334bb163873806676265e946ec2-2996123864724853759.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2bef21c3-8f00-4cd2-a8a3-9a349d0d22e4', '5d9bf876-f0a7-48b1-ad09-c38dc64b2378', 'IMAGE', 'https://cdn.chotot.com/IF6R9RN66wsDY3oCCY4SiLTe9COPzJF8MC6Bw5ERaq0/preset:view/plain/8c9d6c41af794e62181109647f8564d5-2996123864640361768.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cf9ddb32-677f-41bf-9693-af7dd324de36', '5d9bf876-f0a7-48b1-ad09-c38dc64b2378', 'IMAGE', 'https://cdn.chotot.com/t4EyRHmTw62oTP8ireGKiN24hs5ipl9gdKieinJZVw8/preset:view/plain/3b027caa2f27a56eaf94c33bfff1af27-2996123864679952164.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('b96a12ef-8d95-449d-b461-44fb21cc8568', 'P_133003006', 'APARTMENT', '❤️ CHO THUÊ CĂN HỘ TÂN BÌNH APARTMENT – 2PN, 2WC – DỌN VÀO Ở NGAY 🔥', '❤️ CHO THUÊ CĂN HỘ CHUNG CƯ TÂN BÌNH APARTMENT – FULL NỘI THẤT, DỌN VÀO Ở NGAY 🔥

🏡 Địa chỉ: 32 Hoàng Bật Đạt, P.15, Q. Tân Bình
📐 Diện tích: 70m²
🛏️ Thiết kế: 2 phòng ngủ – 2 nhà vệ sinh

✨ Ưu điểm nổi bật:
✅ Full nội thất đẹp, chỉ cần xách vali vào ở
✅ Căn hộ rộng rãi, thoáng mát, phù hợp gia đình hoặc nhân viên văn phòng

💰 Giá thuê: 10 triệu/tháng

📲 Liên hệ/Zalo: 🤝
Nhanh tay liên hệ để xem nhà thực tế và nhận nhà ngay!', 'UNDER_OFFER', 'Quận Tân Bình, Tp Hồ Chí Minh', 70, 10000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d3c19112-250d-4b8a-865f-87ed0017631d', 'b96a12ef-8d95-449d-b461-44fb21cc8568', 'IMAGE', 'https://cdn.chotot.com/tY6iddr7PmEHQ8H2JeZPBPg-IxRq3HEQj-JoGtrlyLA/preset:view/plain/04db449b5e25b7673eb0e6c71fcd94ac-2996124013137073448.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5a094336-3054-4353-9ec9-9c1599153479', 'b96a12ef-8d95-449d-b461-44fb21cc8568', 'IMAGE', 'https://cdn.chotot.com/XjaZ-3N34o3FYXTPjsBZCNPU2lhGRHJD3ssb0U9gft0/preset:view/plain/5e28d7a6fc7a5cbdd29dd2ad32879aea-2996124013143150183.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('123dcb52-2a83-461d-8f63-b009faf49812', 'b96a12ef-8d95-449d-b461-44fb21cc8568', 'IMAGE', 'https://cdn.chotot.com/uo2Xh8fVkkQxK0QvBHywPAFftYYoWzJm-rDzESP5rMk/preset:view/plain/e1fc74fb8abb5347b76a6716cd22c33d-2996124013093366711.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d61053a5-8756-4b44-a55d-ad15cd6f306d', 'b96a12ef-8d95-449d-b461-44fb21cc8568', 'IMAGE', 'https://cdn.chotot.com/sBpvQISfavkzFqUdDoniZFxM0fzYtWpzT1esD4kjbQk/preset:view/plain/8ec00e1cc247d44208bb965c8465f45c-2996124013152323961.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6100b634-a020-4fbc-aa58-fcdd8af26678', 'b96a12ef-8d95-449d-b461-44fb21cc8568', 'IMAGE', 'https://cdn.chotot.com/1fvAoUut7qLQg_HS-w1Dk5ZKnGa_Z132w8Y3WM_0S_U/preset:view/plain/ef8d53f30d98b74ebf561b33ac1ebfa7-2996124013209241060.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('171b61d7-4752-4153-a6d8-7bb0fde2d0b5', 'P_133524872', 'APARTMENT', '🎉SIÊU PHẨM STUDIO Full Nội Thất - Máy Giặt Riêng - Ngay TÔ HIỆU', 'Dự án: 
Thông tin chi tiết: 🌟KHAI TRƯƠNG  STUDIO BAN CÔNG MỚI 100% - FULL NỘI THẤT - SIÊU XINH🌟

Địa chỉ: Âu Cơ - Kênh Tân Hoá - Luỹ Bán Bích - Lạc Long Quân - Lê Đại Hành - Thuận tiện di chuyển ĐH Văn Hiến - Quận 11 , Quận 10 

- Giáp Âu Cơ thuận tiện di chuyển Tân Bình - Sân Bay ,…

- Thang máy - Nhà mới 100% - Máy giặt riêng cho phòng BAN CÔNG 

- Giờ giấc tự do - Không chung chủ - Thuận tiện di chuyển các quận 

📞LIÊN HỆ SDT BÊN DƯỚI ( Thành Truyền ) Em hỗ trợ ngay , nhanh chóng!!', 'SOLD', 'Quận 11, Tp Hồ Chí Minh', 28, 5500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dde4b644-9569-4570-99b0-2fa47e3f0779', '171b61d7-4752-4153-a6d8-7bb0fde2d0b5', 'IMAGE', 'https://cdn.chotot.com/YIJZBkXDIOwaVhFtNUCK4XJSieNuOfhseZl1L_uaXL4/preset:view/plain/8a8f2563d981b5b8a23d28443cc82103-2992942761752321318.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('50b5daba-37b3-4220-a49e-8a4f13bfc6ec', '171b61d7-4752-4153-a6d8-7bb0fde2d0b5', 'IMAGE', 'https://cdn.chotot.com/1yzb2Hbod_dmSkR8GCRY9d7YCq35SVNMjBGh6oko-M0/preset:view/plain/7c18aa92ff1acb04aa2df9d60a35105f-2992942761754228237.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7e7ed496-ac78-4f4e-8a02-c6c0b70fc91b', '171b61d7-4752-4153-a6d8-7bb0fde2d0b5', 'IMAGE', 'https://cdn.chotot.com/2AaR9-JTaJx0MFejc0vMEPdPXkBsXNDRMwcvyDejzs0/preset:view/plain/e03fc281b6f0bd4fb3876082e3ee834d-2992942761726918711.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2ad1a2dd-edf6-42a0-8d45-301a7b3ab4b6', '171b61d7-4752-4153-a6d8-7bb0fde2d0b5', 'IMAGE', 'https://cdn.chotot.com/PvjC4mMRf6AbEIbn4eFVsiLOZQMVX8DngdN0Q6GcMuQ/preset:view/plain/cec2ddff315f7cefb9028735e0ec735e-2992942761986761566.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('86f233f0-ea88-4c47-b899-7e0e4711bed1', '171b61d7-4752-4153-a6d8-7bb0fde2d0b5', 'IMAGE', 'https://cdn.chotot.com/_nMAcjOFRextgRkpz94lxq3Xo_84LL9-uOOzPKA6W0Y/preset:view/plain/0b072f3fc7aa8b13eb86f438c592ddfd-2992942761958384577.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('36bdcb6f-5f1a-4fd9-ba86-dc394f2767bc', 'P_133941040', 'APARTMENT', ' DUPLEX MỚI KHAI TRƯƠNG – GẦN CẦU TRẦN QUANG DIỆU', '✨ DUPLEX MỚI KHAI TRƯƠNG – GẦN CẦU TRẦN QUANG DIỆU ✨
💸 Chỉ từ 5X 🛏️ Full nội thất, dọn vào ở ngay 🧺 Máy giặt riêng từng phòng 🌿 Nhà mới 100%, không gian rộng rãi, thoáng mát
📍 Gần ĐH Kinh tế TP.HCM (UEH), ĐH Sài Gòn (SGU), ĐH Mở TP.HCM (OU)
#duplex #fullnoithat #maygiatrieng #canhochothue #vivuhome  #UEH #SGU #OU #tphcm
', 'SOLD', 'Quận 3, Tp Hồ Chí Minh', 35, 5300000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5562bea2-726a-43be-853c-b768b972032c', '36bdcb6f-5f1a-4fd9-ba86-dc394f2767bc', 'IMAGE', 'https://cdn.chotot.com/Y6RXGGxu29FSF-gw0gLFWGNolXCpFoHZ-AvnaNnpQbo/preset:view/plain/196af72f222cf73a8d92dfccb12d066f-2996123825823199012.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c8aa2907-2f0b-4f9a-96da-a16b52c01bbd', '36bdcb6f-5f1a-4fd9-ba86-dc394f2767bc', 'IMAGE', 'https://cdn.chotot.com/S9bUmdx5r-jH91xNwJML8tV1GJepumw6k1cK2XpIAcE/preset:view/plain/fa77402c6839a98ed5f8c0ec1ed99689-2996123825889396196.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c6620441-6070-4a43-8507-d9c001c58f27', '36bdcb6f-5f1a-4fd9-ba86-dc394f2767bc', 'IMAGE', 'https://cdn.chotot.com/q_RfKSAMc_TRaM80QMBLJYQQhN7w-u_YCQ8pl96ODqI/preset:view/plain/2e105a44664d77882402bd6cc0582c65-2996123827350216792.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e0e064b1-e517-4c65-bb7b-57cdc3eb0e6c', '36bdcb6f-5f1a-4fd9-ba86-dc394f2767bc', 'IMAGE', 'https://cdn.chotot.com/6z2MK3I83pd9PmW6jTc8MffFrlU9vVovgzC97XAvjac/preset:view/plain/bf8d3972826e9baeab762f26dedf4419-2996123828323200804.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('70a42646-86f7-4131-9602-885787e8a114', '36bdcb6f-5f1a-4fd9-ba86-dc394f2767bc', 'IMAGE', 'https://cdn.chotot.com/_GNFWaTcEDl8q5K8Ibr2LezTunJkeowAO8-UrUsqgMo/preset:view/plain/dad51ff264d5c27ebd843a803df7e636-2996123828773886105.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('34e1d826-738b-4525-92cf-c85ade842b74', 'P_133941022', 'APARTMENT', 'CĂN HỘ DỊCH VỤ FULL NỘI THẤT CÓ BAN CÔNG RỘNG', 'Dự án: 
Thông tin chi tiết: CẬP NHẬT DỰ ÁN MỚI
- Địa chỉ: 162 Nguyễn Duy Cung, Gò Vấp
Nhà thang máy
Nội thất: Full như hình, máy giặt riêng, ban công
- Điện 4k
- Nước 100k/ng
- Dịch vụ 150k/phòng
- Xe free', 'SOLD', 'Quận Gò Vấp, Tp Hồ Chí Minh', 30, 5200000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d6ba84b4-91f8-4bd7-b482-4eec892b8fb0', '34e1d826-738b-4525-92cf-c85ade842b74', 'IMAGE', 'https://cdn.chotot.com/jFEHpinHnWdYW3aPVWeQ6i2xq6sdPqPkV63FYBFGVOw/preset:view/plain/bbbef3f90b00a626e3b26fd0a5dd0f7d-2996123573556447801.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('10a0d929-428b-4399-8d05-4155b01fa302', '34e1d826-738b-4525-92cf-c85ade842b74', 'IMAGE', 'https://cdn.chotot.com/P7HAp3dtlDz3RJuPjCMBgJhN7vxP6aKovrUVK5bz8JI/preset:view/plain/61944a76cb52fe2ae4a3d9e3dcaab3c5-2996123573657317156.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a8ab4344-1c2b-4b7c-b58d-556c148ddce6', '34e1d826-738b-4525-92cf-c85ade842b74', 'IMAGE', 'https://cdn.chotot.com/PnoDKDI_Dhwg9OTqG5LEbX_Jboov_7o74denr1UVSzo/preset:view/plain/edc0c26ab7645bfe3d8378bd9519cfa0-2996123573922469969.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c5eb86c0-9e7e-4f44-8f5d-793fa8fb7d64', '34e1d826-738b-4525-92cf-c85ade842b74', 'IMAGE', 'https://cdn.chotot.com/uyqffnpgE9PWVzBqRFGRDgue1wiYNRYHo7PrkL1vTNA/preset:view/plain/9d3fa6a415eca7243fb1c556a4920999-2996123574110060914.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b729ff9d-cdf2-43e8-ae96-c20b19368d62', '34e1d826-738b-4525-92cf-c85ade842b74', 'IMAGE', 'https://cdn.chotot.com/ulStqdO55m1jJwfpQDEEo_1hyY4YbKpxje9Gh1J4IsY/preset:view/plain/54323089e99400c16ae6d55fa1b46393-2996123573707512304.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8dab5e0e-b1fa-4537-a4fd-a641a326f0e4', '34e1d826-738b-4525-92cf-c85ade842b74', 'IMAGE', 'https://cdn.chotot.com/1L6GBwWIWBEJQrA4-Omi7Q1SV7ama-gLaTlD8KRA-bI/preset:view/plain/7dd9a678c9c7c24763af81c091ddbd9e-2996123573657083960.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('590a4d05-3141-497c-9bf1-545139c739ff', '34e1d826-738b-4525-92cf-c85ade842b74', 'IMAGE', 'https://cdn.chotot.com/dXMVNfXHOUIEtS0-sthCb0a3o5hK50IoIWwx7dnHZqY/preset:view/plain/d2c8a6e331c1c3c22101006b01989185-2996123573673950709.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0cfc5770-2cd6-40a1-b1a9-3b8c79ac6112', '34e1d826-738b-4525-92cf-c85ade842b74', 'IMAGE', 'https://cdn.chotot.com/oy8WlouRyQUm5Hzlhe1RqFCnn2hJeGP8r4lE7NgM8MU/preset:view/plain/30eb6be4426a3483787636345ce0d763-2996123573657289011.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('64ce445e-2089-4740-9b2a-97bf2ebf9c62', 'P_130250125', 'APARTMENT', 'Duplex Giá Sinh viên Quận 7  Gần sát đại UFM', 'Nguyễn Thị Xiếu Quận 7 - Sát bên KCX Tân Thuận - cầu Tân thuận- ĐI BỘ SANG UFM 

- Thang máy, hầm xe, mặt tiền đường 
- Đầy đủ nội thất cao cấp , cửa sổ lớn thoáng mát sạch sẽ 
- Sát bên Quận 4 - Tiện sang Quận 1, cầu Khánh Hội
- Ở được 3-4 bạn thoải mái
- Không chung chủ, giờ giấc tự do
- có giặt sấy', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 35, 4200000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('51190ea5-f2be-4254-9b9e-bc87094ae1b6', '64ce445e-2089-4740-9b2a-97bf2ebf9c62', 'IMAGE', 'https://cdn.chotot.com/gl8rTdUzyioyY4Kb0QjuaBFD42xBMFNi4_Wrg2WnLTQ/preset:view/plain/8260f02234f538ac38dd1789414cd544-2966681191231727782.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3ab5222c-bb44-45de-be4e-d8ba1872f48a', '64ce445e-2089-4740-9b2a-97bf2ebf9c62', 'IMAGE', 'https://cdn.chotot.com/4m2-PC0PXeu7zHlByANcH6HMiH8OTLO66m-2e8rrW0I/preset:view/plain/13d7cdb34a4f9ca3df6e9769abbb9adc-2966681191325713623.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('774dabd5-efa6-4a33-984d-e452179e26ff', '64ce445e-2089-4740-9b2a-97bf2ebf9c62', 'IMAGE', 'https://cdn.chotot.com/N4QQWXcsS5XyHwMDNY-0pI3NjIPLB7rm_SbMlwfl6HQ/preset:view/plain/40c1bed0683d3caafdaa1387f98dc0f8-2966681191072344984.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('b5e81a8a-0dc6-4aab-a227-26ca83e2fdb1', 'P_132328194', 'APARTMENT', 'CHO THUÊ CĂN HỘ TOPAZ ELITE 2PN 2WC FULL NỘI THẤT GIÁ 13TR/THÁNG', 'CHO THUÊ CĂN HỘ TOPAZ ELITE – 2PN 2WC  – FULL NỘI THẤT – 13TR/THÁNG
Full nội thất, dọn vào ở ngay
Nhà rộng rãi, thoáng mát
Khu an ninh, tiện ích đầy đủ
Địa chỉ: 232 Tạ Quang Bửu, Phường Chánh Hưng, Quận 8
Liên hệ: Khải – ***
#TopazElite #ChungCuQuan8 #ChoThueCanHo #CanHo2PN #FullNoiThat #vtnewland', 'SOLD', 'Quận 8, Tp Hồ Chí Minh', 60, 13000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('70d2970a-e581-49b5-bf21-ec90885b7506', 'b5e81a8a-0dc6-4aab-a227-26ca83e2fdb1', 'IMAGE', 'https://cdn.chotot.com/jswnnTBQ6y8rG9j1eoTpNlHDkK6EM1prznWb4MZyw0Y/preset:view/plain/7033016293b3795f0302c1505f66c0f0-2983847511983772767.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5a2e341a-3724-41b1-bf0c-b18879adf37c', 'b5e81a8a-0dc6-4aab-a227-26ca83e2fdb1', 'IMAGE', 'https://cdn.chotot.com/onyJ1P9yJBH_MF7mWq3dNsoJBnfoB2_Y6tac5rFCVTM/preset:view/plain/2dbbf01c74df9fd31b54a15fadba8a60-2983847511760999952.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('311c92d5-3511-46fd-80d8-a8e54540078b', 'b5e81a8a-0dc6-4aab-a227-26ca83e2fdb1', 'IMAGE', 'https://cdn.chotot.com/gdl67i-7raoQVkEnwTJEvkvjqxc-Ws47Gwow4GTxsgI/preset:view/plain/78a45ccffe138b6a8c4955d6d3da9842-2983847513002579472.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('df784425-3e38-40ac-bb7c-7008780d7829', 'b5e81a8a-0dc6-4aab-a227-26ca83e2fdb1', 'IMAGE', 'https://cdn.chotot.com/aBL5anAph8tRuJydC_l54e3G15RwWNsToiy8BPa6tdI/preset:view/plain/691301d1cd8866aa15252a6fe5422222-2983847513847764272.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('507cb7ad-cd48-4b32-9888-6b36f6f83647', 'b5e81a8a-0dc6-4aab-a227-26ca83e2fdb1', 'IMAGE', 'https://cdn.chotot.com/RkJNKc59mGmSqVgHtTzYt_FL0AmKtLpj3_OtEDUS3SQ/preset:view/plain/faf9ba6bebbd1b697a6adb806bcba82e-2983847514437181282.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a998aa11-b8c0-44cd-9d22-c8e2dec29fef', 'b5e81a8a-0dc6-4aab-a227-26ca83e2fdb1', 'IMAGE', 'https://cdn.chotot.com/91b9KXWhz2Dzxwktp_fHb_Bo-LaRC2F0hZ4k07D5r0A/preset:view/plain/c9067077ecdfaab47f41dddcbf361acb-2983847514953471071.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e660f93c-e887-44c7-840e-354dcabffdf5', 'b5e81a8a-0dc6-4aab-a227-26ca83e2fdb1', 'IMAGE', 'https://cdn.chotot.com/A8bvr9R8lRM0hnsa19CYKpfE4EuySjHKlkTwPe8HLyM/preset:view/plain/4ac2860ba5b5b555b562e2951d7fc8ae-2983847515624625247.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b6c651b0-f615-4fed-9762-9fead9a22a26', 'b5e81a8a-0dc6-4aab-a227-26ca83e2fdb1', 'IMAGE', 'https://cdn.chotot.com/U0vSIz1vgq0h9-zluBwPIOp7givKsdZzET02nO4Tux4/preset:view/plain/1aa29bc10abbcb1d5bf7d67782ab3685-2983847516274333200.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('90fffb41-e76a-407c-80d9-22a52764a268', 'P_119622231', 'APARTMENT', 'Q7 RIVERSIDE 2PN 9TR NTCB VÀ FULL NT 10TR, NHIỀU CĂN', 'CHÍNH CHỦ RA NƯỚC NGOÀI CẦN CHO THUÊ CĂN OPAL BOULEVARD - 2PN NỘI THẤT XỊN
- Diện tích:68m2
- GIÁ: 10TR FULL NT, NTCB 9TR
- Bao phí quản lí 1 năm
- Trang bị nội thất đủ
Hơn ngàn tiện ích hiện đại như: Gym, Spa, hồ khoáng nóng, Shophouse đa dạng, Chuỗi BBQ ngoài trời,...
Hồ bơi siêu đẹp, phòng tập GYM, Nướng BBQ ngoài trời, Khu vui chơi trẻ em.
Bách hóa xanh, winmart, sapa & Nail, lớp học trẻ em,...
Pháp lý 100% đã có sổ, công chứng sang tên ngay.
Hỗ trợ tư vấn chọn căn giá ***, thủ tục hồ sơ vay ngân hàng, hỗ trợ thủ tục mua bán từ A - Z cho tới khi sang tên cho khách.', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 68, 9000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7678274f-1070-4dcf-bd3f-595336ccb908', '90fffb41-e76a-407c-80d9-22a52764a268', 'IMAGE', 'https://cdn.chotot.com/jbs3DUhFSTrN2bbLO28M0AbDmEPXeS8iAixqpD0Bw9Y/preset:view/plain/7e3d05b09b4c8b0e765af600e695aa22-2903647057879091879.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b4fde269-28fe-4823-8823-65d5f5d657ac', '90fffb41-e76a-407c-80d9-22a52764a268', 'IMAGE', 'https://cdn.chotot.com/QrQhsUfHt8cA2_hOMf_KTQNE-xNLrwxLHKhiCM8090M/preset:view/plain/5d59aa4f89d6483831854472763dc140-2903647063705503119.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5b818af5-37d2-4136-bc60-9e4ed099dbf1', '90fffb41-e76a-407c-80d9-22a52764a268', 'IMAGE', 'https://cdn.chotot.com/47mOS-BOT6X-JZsSVdrsMEsPRiyou_RAaevhgVDp5XI/preset:view/plain/515fc71b79a380cb9cc89b80a1d81234-2903647064039594433.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8bad1e22-9276-48ff-aef4-34526b784eea', '90fffb41-e76a-407c-80d9-22a52764a268', 'IMAGE', 'https://cdn.chotot.com/TkhhdguGJ9i6yO6GG5gIx0MB8erPEn2YjZnNZnIM2eM/preset:view/plain/55fa8b909920de0404252e80c7c39bd1-2903647063684401831.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a6255478-0dbb-4817-bd66-2b40814195c5', '90fffb41-e76a-407c-80d9-22a52764a268', 'IMAGE', 'https://cdn.chotot.com/IgUpNrArTiW4Rw_er15h5MsW0D3Wv7ayE6iCRuEVoSA/preset:view/plain/7ed6ffc1d1cc7fc8b4791084aa30cec7-2903647064015369837.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('3467c202-fff3-4307-83ef-5ee1a5acc853', 'P_133941001', 'APARTMENT', 'Bán căn hộ The Estella 179m2 quận 2 hcm', 'Dự án: 
Thông tin chi tiết: Cần bán căn hộ The Estella 179m2. Bàn giao full nội thất, căn góc, tầng thấp.', 'UNDER_OFFER', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 179, 19500000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d660b82d-a6d6-4ab2-bebd-703dca03d226', '3467c202-fff3-4307-83ef-5ee1a5acc853', 'IMAGE', 'https://cdn.chotot.com/NGH1xPIgmViLDNLfm2gZ6Ceef05DJXkEQx6dP5q827I/preset:property_project_small/plain/92_sample_house_3.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d2b264a2-451c-4c38-a3a9-872c34a777db', '3467c202-fff3-4307-83ef-5ee1a5acc853', 'IMAGE', 'https://cdn.chotot.com/k6LKiWAQnYqQozcoXQCIyMeefxkEPjvx-hK46UdE0lU/preset:property_project_small/plain/92_facilities_2.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('677da716-fd22-46cf-91c9-521a88b2276d', '3467c202-fff3-4307-83ef-5ee1a5acc853', 'IMAGE', 'https://cdn.chotot.com/FVoCgRdJjiLSpkP9GA0BJ6GZvqnKALeygl1kVf3iygQ/preset:property_project_small/plain/92_overview_1.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('776ec30d-6564-47f9-b5c6-b57f1f035291', 'P_132175772', 'APARTMENT', 'CHO THUÊ CĂN HỘ TOPAZ ELITE 3PN 2WC 95M2 FULL NỘI THẤT GIÁ 16TR/THÁNG', 'CHO THUÊ CĂN HỘ TOPAZ ELITE – 3PN 2WC – 95M2 – FULL NỘI THẤT – 16TR/THÁNG
Full nội thất, dọn vào ở ngay
Nhà rộng rãi, thoáng mát
Khu an ninh, tiện ích đầy đủ
Địa chỉ: 232 Tạ Quang Bửu, Phường Chánh Hưng, Quận 8
Liên hệ: Khải – ***
#TopazElite #ChungCuQuan8 #ChoThueCanHo #FullNoiThat #GiaTotQuan8 #vtnewland', 'AVAILABLE', 'Quận 8, Tp Hồ Chí Minh', 95, 16000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8a9f743d-3098-4c8c-850d-552060905147', '776ec30d-6564-47f9-b5c6-b57f1f035291', 'IMAGE', 'https://cdn.chotot.com/xBBMvwrVpRujDGFgo0FtVggeAbsWP_Y3B6yk1hXgEUk/preset:view/plain/67a9d8b12ac685f0684d3b8989acd8e8-2982774339081995055.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f34f5202-5f41-4614-9d31-afbaa2dfc5a4', '776ec30d-6564-47f9-b5c6-b57f1f035291', 'IMAGE', 'https://cdn.chotot.com/8TjKxyuWwNNDit7CrFXnqtCwjoKCahpXjvKTsGNvRLI/preset:view/plain/b1a6cd42195ff88362eaa5fd522081ad-2982774339247230745.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('092358a2-2a99-4b2c-8699-fae76340b907', '776ec30d-6564-47f9-b5c6-b57f1f035291', 'IMAGE', 'https://cdn.chotot.com/J72JrX_csCGIE-wCVQL1NZCIPULIBn3iSVGNrynrVQ0/preset:view/plain/f19a2f1c476583f5fa9de125866b4964-2982774341262595772.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d88d0a20-30a9-4ecc-a67d-b42306d38c1c', '776ec30d-6564-47f9-b5c6-b57f1f035291', 'IMAGE', 'https://cdn.chotot.com/hAqVH4Tnvvp0yTReKQxmfnfe3_JljT2SlR3QyQiL9zo/preset:view/plain/c2e7d2e869ca7763a241a8c40751ccab-2982774340671124489.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a6094b9b-379a-42eb-a3d9-ca58f444d5a0', '776ec30d-6564-47f9-b5c6-b57f1f035291', 'IMAGE', 'https://cdn.chotot.com/fkYKE5d9-ur-TMXjMX7dZzt9XqFjzB9tx7O2yZ8IdbI/preset:view/plain/028eb0f3b21f63222e7d81b1be29ed41-2982774342634124297.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0e7e4df3-2fa1-433f-81f3-0e2c0932e0b4', '776ec30d-6564-47f9-b5c6-b57f1f035291', 'IMAGE', 'https://cdn.chotot.com/Oto0aek6AbrxtZljT1UD1dktLJ0wMt-c2_ffcZ9SZk0/preset:view/plain/3ba1f4f21b155309f3e9251361bb67e1-2982774343277799749.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5e2364c2-8ffc-4fa8-b663-f5587292d753', '776ec30d-6564-47f9-b5c6-b57f1f035291', 'IMAGE', 'https://cdn.chotot.com/A_9TW5NuNdTmuVyRimL1-S5vZNELSqW7wwkTHDSln_U/preset:view/plain/10fda9350844ac8298351508565dcedb-2982774345004483375.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('fd469ba5-cfec-411b-8f44-9d0beb344e9a', 'P_120999236', 'APARTMENT', 'Q7 RIVERSIDE: 2PN2WC CHO THUÊ SỚM 9TR NTCB, FULL NT 11TR (1PN 8TR)', 'Cho thuê Q7 Riverside
- Có máy lạnh 9tr,nhà trống 9tr, Full đồ đẹp, nhà sạch, đồ mới 99% full nội thất 11tr
- Có thể vào ở ngay.
- View siêu siêu thoáng.
- Giá cho thuê tốt
- Đầy đủ đồ và thiết bị gồm: Bộ tủ bếp trên dưới, bếp từ, hút mùi, điều hòa nóng lạnh, tủ lạnh, giường đệm, sofa bàn trà, máy giặt, giàn phơi, tivi, rèm cửa...

Liên hệ em để xem nhà trực tiếp hoặc xem thêm nhiều căn hộ giá tốt khác đang cho thuê', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 68, 9000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f53777ab-4821-40d3-a895-0b0cd9819b1e', 'fd469ba5-cfec-411b-8f44-9d0beb344e9a', 'IMAGE', 'https://cdn.chotot.com/YM8oFGn4YpSrUEIVICa2Un9w1ckk-0du2g5i9Em0Lbw/preset:view/plain/8946dc7ba979cd4aacb363c4c4311c82-2905245938893182708.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dc8c1cb3-bd98-4006-84f0-fc9ea14d027e', 'fd469ba5-cfec-411b-8f44-9d0beb344e9a', 'IMAGE', 'https://cdn.chotot.com/_Wh8p8X8anHdiEDWO6aohrNhV9iwWtmnmGczkSWYu6I/preset:view/plain/56d1aaa27f8940e8f03ea70a9cf4390b-2905245945391599478.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8fa4f36f-ac0e-4b71-87f6-1c84631c61e3', 'fd469ba5-cfec-411b-8f44-9d0beb344e9a', 'IMAGE', 'https://cdn.chotot.com/DLga1SIiFW1dLEC9hgPb94JZY8RjHGTJgJXarT8sWrA/preset:view/plain/f1b9bf36b104d5cf583a98605d4073b0-2905245946316771357.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8c0c522a-23a3-47fd-a82e-41f3f8ac2259', 'fd469ba5-cfec-411b-8f44-9d0beb344e9a', 'IMAGE', 'https://cdn.chotot.com/qprSrp4iKvh10hfJGq3J8mjqyRrO6n8r3EgnM3qSh8c/preset:view/plain/fdc62a162a648a231bfbbcb514f833e7-2905245945691353761.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1b7e11f1-3c54-4b2b-b3a8-73ab41f67839', 'fd469ba5-cfec-411b-8f44-9d0beb344e9a', 'IMAGE', 'https://cdn.chotot.com/HA6ZfPJvZWSFnHDb6ZIUXZFHv64VQrssfhBD9tRmSPQ/preset:view/plain/e8cb78bffdfa198d6bb0039b84e3c0ca-2905245945529392429.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d8cf15f3-e999-4fee-8c5d-b25842e26dfd', 'fd469ba5-cfec-411b-8f44-9d0beb344e9a', 'IMAGE', 'https://cdn.chotot.com/Y9h7aASuaMib1ugyAaWL7BNnstPznFjaeFzkJqJ3r2s/preset:view/plain/2c0f8de2f422ecdb33c837eb2d2c9816-2905245945999520656.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b860a853-baa3-4b24-a020-c202df10d0a4', 'fd469ba5-cfec-411b-8f44-9d0beb344e9a', 'IMAGE', 'https://cdn.chotot.com/T69a-DiJIGxqLInOQpkvuRs_LieE9XQLfFMlf5XaJ0U/preset:view/plain/6001201ab53ad30b884c5dd697d654a7-2905245945523637540.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6b586e47-ab38-47e0-a6fd-beb8b6c509b9', 'fd469ba5-cfec-411b-8f44-9d0beb344e9a', 'IMAGE', 'https://cdn.chotot.com/Ok5IL-r6eMSqf3HV6nUFI8CoGDagOUcWWgCnF-eqNAQ/preset:view/plain/e4adad5d8091faa2f1c7041dd6812685-2905245945444942194.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f150ebd0-4f27-45b0-a525-5810755a825f', 'fd469ba5-cfec-411b-8f44-9d0beb344e9a', 'IMAGE', 'https://cdn.chotot.com/GynXaxW-NcI3nPDX3TCMK0u7H5wfGK8d7kamTj9f6nU/preset:view/plain/339e43f5bdeb6d269e3096122f810c2e-2905245945566156421.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('93393eeb-d869-41e6-8e25-f65d264e2fdc', 'P_133940981', 'APARTMENT', 'Cho thuê căn hộ 1 PN, Q2, Có ban công, Có cửa sổ', '1PN - 📍 xxx/xxx Đường Số 6, Phường An Phú, Quận 2 (Phường Bình Trưng), Thành phố Hồ Chí Minh - 50m²
✨ Có ban công, Có cửa sổ
----------------
📝 PHỤ PHÍ:
- Điện: 4.000
- Nước: Giá nhà nước
- Gửi xe: Miễn phí
', 'UNDER_OFFER', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 50, 11000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fd158f79-a431-401b-8da4-dc80691d7527', '93393eeb-d869-41e6-8e25-f65d264e2fdc', 'IMAGE', 'https://cdn.chotot.com/BoNFKcescBiJu2pwb_dduPBihhYiVavGScJIT-lLo-U/preset:view/plain/79a26d3a61b0997be2f99567b75247d7-2996123337999897599.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0a17b4f4-38f5-47c2-8499-a0d237079ffa', '93393eeb-d869-41e6-8e25-f65d264e2fdc', 'IMAGE', 'https://cdn.chotot.com/iwLGxbBwIWPZjhGPHd8qzZfN6G0b36i2Ct2a8uuQO6w/preset:view/plain/efecf476ac84fb30f764a9f49b11da16-2996123337386769133.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('013a0485-b674-40f9-9d0c-0ea24e5fa673', '93393eeb-d869-41e6-8e25-f65d264e2fdc', 'IMAGE', 'https://cdn.chotot.com/7LcuBFpXDL2bhsWXutKrh3O40ltSCIeq0HOCbvYDoXw/preset:view/plain/c2f0c57517b4c8599f2b679500af0231-2996123337537964409.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7919cd14-1ab4-4417-b03e-36f803d3d90a', '93393eeb-d869-41e6-8e25-f65d264e2fdc', 'IMAGE', 'https://cdn.chotot.com/_dmZVMFMD-FUgB7NoMFA_CDiwE_xWQp5eCBqmFB36mA/preset:view/plain/1da21854b3d64425170945ff96334b84-2996123338050541649.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('61908b12-8807-4961-bba1-19ad27f2c156', '93393eeb-d869-41e6-8e25-f65d264e2fdc', 'IMAGE', 'https://cdn.chotot.com/I555Jsa8LLVHafgZHFVjxQPrdWcToOPae-3XRHOrrgk/preset:view/plain/142d3ab635fdebccff5f9783736554ba-2996123337547683993.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d005b74d-ddc8-49d3-b8d4-6b5ab70ab67a', '93393eeb-d869-41e6-8e25-f65d264e2fdc', 'IMAGE', 'https://cdn.chotot.com/NryTc5_brS1s9MW9lM9c1qo7A5uzo1h_FIAnIcK0feI/preset:view/plain/6549740c2ee470225980f053036595c2-2996123337622529060.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('74b3aaab-c959-4f0b-aec7-5520cac26294', '93393eeb-d869-41e6-8e25-f65d264e2fdc', 'IMAGE', 'https://cdn.chotot.com/c3MVkvU9qwa7ezZ8vBXhfFsvR4v2pL4TTCmQZKnvUO4/preset:view/plain/34e56d0e41cb506641eeda877c36656b-2996123337569214552.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('66124ecc-ab8c-4988-b7e5-9dc1742b3ba4', '93393eeb-d869-41e6-8e25-f65d264e2fdc', 'IMAGE', 'https://cdn.chotot.com/CAOCLJwHfxPCItYjQiuauTgn7Xj2EictVRj839tPxMs/preset:view/plain/4bfaa66b049525f27a480f65cebf50f2-2996123337496118756.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('6f731ca3-11f5-4b36-ba46-5392ca22cb09', 'P_133902686', 'APARTMENT', 'Khai trương duplex ban công mới', 'Dự án: 
Thông tin chi tiết: Toà nhà có thang máy - hầm xe rộng

Không chung chủ - ra vào vân tay

Đi Hutech , Hồng Bàng, UEF chỉ 3-5 phút

Khu vực an ninh, dân trí cao

Tiện đi Quận 1 - Quận 3 - Quận 2 - Phú Nhuận', 'SOLD', 'Quận Bình Thạnh, Tp Hồ Chí Minh', 40, 5600000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f0c95891-5c8f-4e1d-ba8e-6e9dffdb0b60', '6f731ca3-11f5-4b36-ba46-5392ca22cb09', 'IMAGE', 'https://cdn.chotot.com/VlgfTRdJzsJK9k05KqAlK82ydoefaaXiLCg7YYpIhWM/preset:view/plain/4471e64df6c35427c954f920b6bc5797-2995830281446312313.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5f912e1f-800e-4311-85de-725e26e5d56e', '6f731ca3-11f5-4b36-ba46-5392ca22cb09', 'IMAGE', 'https://cdn.chotot.com/ov1Uru1fsqLwUT_1WOhFs73kdqdjnguM_qJpWZztL0s/preset:view/plain/fe7e11d9325fe14e5871975f19317210-2995830281790477311.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('00cf8263-08ca-42a6-ad36-e77c67817e56', '6f731ca3-11f5-4b36-ba46-5392ca22cb09', 'IMAGE', 'https://cdn.chotot.com/vp8QZppUMQ4yX0-_xMGZkfrIWxDnyYFpwZmbTVsrMBo/preset:view/plain/2fd1890e9427df010fef1cfaa8b7868d-2995830281671722468.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('099ef340-c096-4019-8116-34196e25224b', '6f731ca3-11f5-4b36-ba46-5392ca22cb09', 'IMAGE', 'https://cdn.chotot.com/1ewYeg8873qkTrUCtsVQviZQvjigQh6LxJdp3iBsSBc/preset:view/plain/94e7d303f0d73e69d720cca7836f730e-2995830281737976393.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ebbd023d-1d4c-4271-b054-7c1e15c30bad', '6f731ca3-11f5-4b36-ba46-5392ca22cb09', 'IMAGE', 'https://cdn.chotot.com/yv_He4hent2pXycyhXixk2AMXDmeWJQlNFScaPIj11k/preset:view/plain/e9b93b812291f135c5a567372d256f7a-2995830281587919444.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5166eabc-977e-41df-b108-8a8d58649062', '6f731ca3-11f5-4b36-ba46-5392ca22cb09', 'IMAGE', 'https://cdn.chotot.com/TRm4a8G-VAea-7PYgnG4jyXGDb49tYTFq1YjqLiDG5s/preset:view/plain/8728abf11fae9dff6c481085bb9b4356-2995830281660468484.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d7f8bb5e-1f16-4015-9bce-5eb3c973da00', '6f731ca3-11f5-4b36-ba46-5392ca22cb09', 'IMAGE', 'https://cdn.chotot.com/MZiJnX4sZQAnIEYMsGTRrrpjN7lFSerJ0x8eloS07jA/preset:view/plain/5060931581c1f7deae85297b150f932d-2995830281729976165.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e074fff9-415e-4cd9-9e8d-13f6c0fc9436', '6f731ca3-11f5-4b36-ba46-5392ca22cb09', 'IMAGE', 'https://cdn.chotot.com/gZ49xmZNrbAxwNglaXqOx7EkA2JHNNyGlDKE7nJkkL4/preset:view/plain/ca9c6294eb59947fb79e6324c294f520-2995830281980385727.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d380a2d3-b902-472a-93a8-a8a440548de3', '6f731ca3-11f5-4b36-ba46-5392ca22cb09', 'IMAGE', 'https://cdn.chotot.com/aqtKRJNObZW3Pwma604Fw7VTeolNpW6S0o_S2o2FAYs/preset:view/plain/a87e91b086d6e09bbc88b020a48f9cac-2995830281744819118.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('b308ab97-6dc0-4070-ac67-86348da8b0a1', 'P_131638415', 'APARTMENT', 'Duplex Giá Sinh Viên Quận 7', 'Dự án: 
Thông tin chi tiết: DUPLEX  SIÊU RỘNG FULL NỘI THẤT NEW 100%
 Quận 7

Phòng rộng thoáng mát phù hợp ở 4 người
Có ban công đón gió lấy sáng
Thuận tiện qua Q4, Q1, Q8
Có khu giặt phơi chung', 'UNDER_OFFER', 'Quận 7, Tp Hồ Chí Minh', 35, 3200000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('797451fe-614f-440e-9ae9-3cdba5fcc9ab', 'b308ab97-6dc0-4070-ac67-86348da8b0a1', 'IMAGE', 'https://cdn.chotot.com/E79mwbV8nK4o08YSboqpphgAwvrwnruCi-mGv-aIYwM/preset:view/plain/01e7804e5df5e4f54689f26f4de3ea10-2984831026629119149.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('71ebeca2-e761-429a-8cee-43e7f6fa31dd', 'b308ab97-6dc0-4070-ac67-86348da8b0a1', 'IMAGE', 'https://cdn.chotot.com/3FKC7VEkj2n5Wee9eFUMxo_HKUPLiYl5sc1XAsyVC2g/preset:view/plain/f18d3b5a9c7da4c2a6511f75c2e9f6fc-2984831026685015249.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e0e1be8d-977a-4093-a098-063bf6a65f8c', 'b308ab97-6dc0-4070-ac67-86348da8b0a1', 'IMAGE', 'https://cdn.chotot.com/MT_uO5AZU-hKI9wvetI3Lyg_qGMM0f9kWplSRqaL_fc/preset:view/plain/59223d8793f0086478143cfd0d42d638-2984831026788444820.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('25e41902-849e-4ec1-8c10-947b58facb85', 'b308ab97-6dc0-4070-ac67-86348da8b0a1', 'IMAGE', 'https://cdn.chotot.com/tEbyA2mD1vZquLkXkdTPaz7sXROZ6F-czN6lFPOcMBY/preset:view/plain/0196adebf0c28e628db94dedda8cb514-2984831026880856523.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4e284a91-189c-4483-94ff-590e88f332aa', 'b308ab97-6dc0-4070-ac67-86348da8b0a1', 'IMAGE', 'https://cdn.chotot.com/JgT9MWc4NHeoTSZCXg-IsuyU0ieoE_HsUd4kHgal4SI/preset:view/plain/f0f4e2fe4965cad17f59bdde654f3953-2984831026936730325.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('d5123d50-1186-4b50-8525-0392dcd4088c', 'P_133819582', 'APARTMENT', 'cho thuê lâu dài căn shophuose', 'Dự án: 
Thông tin chi tiết: Cần cho thuê gấp căn shophuose với dt 69m2  gần đến Metro Thủ Đức gần trường đại học sư phạm kỹ thuật Thủ Đức ngay ngã tư Thủ Đức có siêu thị Co.opmart bán kính 200 m có cây xăng có trường học có bệnh viện rất thuận tiện để mở công ty. spa ngân hàng .làm móng tay móng chân dịch vụ giặt ủi mở quán nước ép trái cây 4 mùa …,vv  liên hệ chính chủ 0903954889', 'AVAILABLE', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 69, 15000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5de5a720-050c-4ae0-984c-4855c4e82825', 'd5123d50-1186-4b50-8525-0392dcd4088c', 'IMAGE', 'https://cdn.chotot.com/0_PPlkLs-pOXFJr_iTJwCeEUORlyAdIfzHF3yh4rlpY/preset:view/plain/d0d0379c468dcba98f35feffa95e8a00-2995223469006442595.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2f8f683f-0b9b-4e21-b09f-198e05abbb6b', 'd5123d50-1186-4b50-8525-0392dcd4088c', 'IMAGE', 'https://cdn.chotot.com/rh0dONTsLV5Dtu4GVKq2r-6J1-Y-2rgHHl3p17xFoxk/preset:view/plain/3bc8ee816e2e3a9440fd71fc77523d27-2995223468883396419.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('673a480a-4f3c-41af-ac2d-fc59633a6b3f', 'd5123d50-1186-4b50-8525-0392dcd4088c', 'IMAGE', 'https://cdn.chotot.com/sCZq2Q7sGC27fL56w-NQQ-ON8iXARK8xt2HUT4yT6fI/preset:view/plain/b0fee6be12ab1a9606f5d2aefc69f55a-2995223468964370838.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d3d2a1f7-20d3-454e-ba81-60fb561ef7ca', 'd5123d50-1186-4b50-8525-0392dcd4088c', 'IMAGE', 'https://cdn.chotot.com/iqkoQGg_oetDWxvIuKs_RVnR2mZ1knBs_y4aDa1qwBw/preset:view/plain/e119b04817d1441ae96c8c7551d91e54-2995223469064667490.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('031b024e-95d0-4862-bba0-8c31d74430a5', 'd5123d50-1186-4b50-8525-0392dcd4088c', 'IMAGE', 'https://cdn.chotot.com/NWVJjUGm5B1CdUtj0RZxBimiO0mOpe0PjVnJE7n1fUQ/preset:view/plain/02d13bb9376d19e43ee8cbaa4ed029d4-2995223470485787504.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0644bd34-ff22-4b1d-9909-b02a22f2052d', 'd5123d50-1186-4b50-8525-0392dcd4088c', 'IMAGE', 'https://cdn.chotot.com/tTxy_9bBwr5Md5GdFBHTALAtYuLcOitNoWxPC0fD_JY/preset:view/plain/15dfd9c8b26f0ff3c731e61dd4f9cec4-2995223470654476682.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('318bd075-8dc3-459e-b17a-6b61cea5f241', 'd5123d50-1186-4b50-8525-0392dcd4088c', 'IMAGE', 'https://cdn.chotot.com/tPb1ZTQA6r8oeOexa6yy_cY31gh0u9A5sdrFQDWXH08/preset:view/plain/bba116dd1131f537a9ff678f1d52a7be-2995224746906211184.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('67cc4528-68bd-4aa4-b85d-b5ee39f17176', 'P_133940954', 'APARTMENT', 'Studio Full nội thất Quận 7', 'Dự án: 
Thông tin chi tiết: STUDIO FULL NỘI THẤT NEW 
100% 4🥔 Giá Thật Không Ảo
Phòng rộng 2 bạn vô tư
Thuận tiện qua Q4, Q1, Q8
Có khu giặt phơi chung', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 25, 4099999, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ea937e16-6c67-4ac2-b8e0-8847e383245d', '67cc4528-68bd-4aa4-b85d-b5ee39f17176', 'IMAGE', 'https://cdn.chotot.com/DPTMwxytQVgzw86-CgTzxa8FtNXawYMadL-LjW5Ok2k/preset:view/plain/1f3cfbfca5dd603146f360f168d86f98-2996123356455803033.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8710ce39-5511-4a2b-86f2-6969bf7fbc3d', '67cc4528-68bd-4aa4-b85d-b5ee39f17176', 'IMAGE', 'https://cdn.chotot.com/np9AFj5PR5Dlmb-nK6xUTXnO6HF45VeAbU1JNLa-Qcg/preset:view/plain/98bdb827a88fa73c8291449eba8480de-2996123356664249069.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ccdb1d3c-2290-41a3-a28c-35ed82a225eb', '67cc4528-68bd-4aa4-b85d-b5ee39f17176', 'IMAGE', 'https://cdn.chotot.com/FvRNkHXpB3Up8nuy4VytID6v2QN4WOF2daVMl1pxoZo/preset:view/plain/9ce7d5c5320fe7d1b5e51d9b639dd7d1-2996123356628328536.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('eec2f067-d5ff-470c-b741-190c37775a25', '67cc4528-68bd-4aa4-b85d-b5ee39f17176', 'IMAGE', 'https://cdn.chotot.com/gQqjsDPf3Y9-n7S37lpmjpj51lxq1ZwG4ZAAV9nhFB8/preset:view/plain/5780356c18d4b0393e904b9736347fd3-2996123357264621972.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bd1bab65-23a1-4ceb-9851-b885e4cc5232', '67cc4528-68bd-4aa4-b85d-b5ee39f17176', 'IMAGE', 'https://cdn.chotot.com/BMj5Xa-ZuZTDafA9FA83oCZ8PNyO5XJxhIxJawU7mwM/preset:view/plain/c0ecefb5ad2d07ccb8c9a39327fe1350-2996123356853528230.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('68e44f0d-843c-4daf-89db-e2bf5c777e39', '67cc4528-68bd-4aa4-b85d-b5ee39f17176', 'IMAGE', 'https://cdn.chotot.com/GKMUz58aXoLQ4VjPgFmOl0L6HQcCnCCHFUl-rAM1qdM/preset:view/plain/6c339494687c4903327ba3daf076ceba-2996123357063311846.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e929d24a-b47f-452d-a173-f672ae0b8ea9', '67cc4528-68bd-4aa4-b85d-b5ee39f17176', 'IMAGE', 'https://cdn.chotot.com/s1_DNrjnrTH5SbrDja2dc7BOxqgSNQBMNYH-yafMs8Y/preset:view/plain/d4c15c719c90ada1fd9e5ef1cb68cd4d-2996123357075654116.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('d46b2296-5c3f-4c3f-b8df-d07b672c8543', 'P_133940950', 'APARTMENT', '💃 CHO THUÊ CĂN HỘ 2PN RỘNG 80M2 Ở NGUYỄN VĂN MAI QUẬN 3', '💃 CHO THUÊ CĂN HỘ 2PN RỘNG 80M2 Ở NGUYỄN VĂN MAI QUẬN 3
✨✨✨✨
✅ Căn hộ cao cấp, có đầy đủ tiện ích 
✅ Có hầm xe, thang máy, bảo vệ, lễ tân
✅ Vị trí căn hộ nằm ở trung tâm quận 3.  Thuận tiện di chuyển tới các quận khác chỉ 5 phút
✅ Có hỗ trợ khách nước ngoài, khách Việt,...
✅ Có hỗ trợ xuất VAT nếu khách có nhu cầu
_____
Liên hệ *** (Lê Duyên - hỗ trợ tìm phòng 24/7)
', 'UNDER_OFFER', 'Quận 3, Tp Hồ Chí Minh', 80, 12500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('17131a0e-6863-447b-b064-694386725310', 'd46b2296-5c3f-4c3f-b8df-d07b672c8543', 'IMAGE', 'https://cdn.chotot.com/IZI5fxT8wl5C3oZTDxgBu4tPy1Vp757wO0zoNdqSSpo/preset:view/plain/fd950b950aaca9af3a5fab39a8990fc3-2996123187557603481.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fc14563e-7b7f-4a39-9fda-2aff5480fbaa', 'd46b2296-5c3f-4c3f-b8df-d07b672c8543', 'IMAGE', 'https://cdn.chotot.com/3KKtV7NBPDBOC9B4TtEU4C6ZjeNBgElwMnBjGXDrYT4/preset:view/plain/cdff38a87ecb8c75ac37ce0b03b60fdd-2996123187463863021.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c5214086-1229-4740-a669-721b40eb0578', 'd46b2296-5c3f-4c3f-b8df-d07b672c8543', 'IMAGE', 'https://cdn.chotot.com/JFcoPQfKpmHXLQEd3nNv5RnEhSCnUu24BP0TysLozzk/preset:view/plain/2d1f5b591348acd497c408fc10d35ed2-2996123188881573348.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e1871b35-cdd1-48f7-b263-a2ba060b49dc', 'd46b2296-5c3f-4c3f-b8df-d07b672c8543', 'IMAGE', 'https://cdn.chotot.com/v6kNDXWZceXf4Yx52GVvbPXgabjoLSFrCXty62oSEyw/preset:view/plain/a329dd21f42dcce7d06526cd4347c357-2996123188983732377.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5764555f-d440-4e64-9570-dfa6304375cc', 'd46b2296-5c3f-4c3f-b8df-d07b672c8543', 'IMAGE', 'https://cdn.chotot.com/l94WOqTR9-wSxgflVKP4AvtCSQ5o6eHOUf7dwqffyN4/preset:view/plain/d7916c6a0c80a657a92b0eaa2e1dce50-2996123190510474239.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d7f6b4b2-fa1e-4ac5-b6a6-f3690e720acd', 'd46b2296-5c3f-4c3f-b8df-d07b672c8543', 'IMAGE', 'https://cdn.chotot.com/liL6Jgj2i_v_8_H8mBpAUIQnew4BSeT3e3R_G7O_jfQ/preset:view/plain/3df637e82e62085e9416ba3252146e6b-2996123190449086552.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f2f4c666-3486-4a8f-9c4b-27790ad57c57', 'd46b2296-5c3f-4c3f-b8df-d07b672c8543', 'IMAGE', 'https://cdn.chotot.com/DgvEA1v68djwPjSvgg020fRJqmuPBQuIMXXbi0KOQO8/preset:view/plain/e9adc6209fc2669c24143a1e7a4a39b0-2996123191774759289.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('52afa6a4-3635-476b-ae94-603589e7f879', 'd46b2296-5c3f-4c3f-b8df-d07b672c8543', 'IMAGE', 'https://cdn.chotot.com/Clm3QT7hNRNb_0fIaSFTJeLoYc8XILOKN0YzZXRahgk/preset:view/plain/155c7c95c02f3e1804c1a22525d78970-2996123192059764824.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cd180738-fbe2-420a-bd15-d93a0f7a274d', 'd46b2296-5c3f-4c3f-b8df-d07b672c8543', 'IMAGE', 'https://cdn.chotot.com/zwcR71YKZegStCUtRDAn4gTjkJubx6S79wK5pM3WuhE/preset:view/plain/3ab31f367ab6dd8947a27ad2a7297044-2996123193295607961.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('4a612297-1d3a-492e-9971-0b2678e8373b', 'P_130984223', 'APARTMENT', '✅Cho Thuê Căn Hộ_1PN 50m2_Bacolny_City View_Gần Cầu Thủ Thiêm✅', 'Dự án: 
Thông tin chi tiết: Hệ thống hơn 1000+ căn hộ khắp các quận chỉ chờ khách iu tới chốt.

✅Hà Dương luxury apartment✅
( Nhiệt tình, Uy tín, Trách nhiệm)
~~~~ ~~~~ ~~~~

✅VỊ TRÍ CĂN HỘ:  Đường Ngô Tất Tố, Phường 22 Bình Thạnb
- Cam kết hình thật + Giá thật
- Tiền cọc: 1 tháng tiền nhà
✅ Giá Phòng: 11.000.000✅

✅Giá Phòng bao gồm:✅
📢Dịch vụ tốt, chỉ cần xách vali vào ở.
📢Bảo Trì, Sửa chữa, Giờ giấc tự do, Hầm xe rộng rãi.
📢gần nhiều tiện ích, dọn vệ sinh thang máy, hành lang mỗi ngày.
📢Bảo vệ 24/7, an ninh tốt, dân cư yên tĩnh, văn minh. 
📢 Có Thang Máy, ra vào bằng vân tay
📢Full Nội Thất đầy đủ các thiết bị cần thiết….
      ...............
✅Ngoài ra, Dương còn cơ số căn hộ xịn xò khác ở Các Quận:
- Studio, duplex ban công, cửa sổ giá từ: 6tr9
- 1PN Đẹp giá từ: 10tr
- 2PN, Căn hộ cao cấp giá từ: 12tr

📲Inbox Dương hoặc liên hệ hotline / nhắn tin Zalo qua SĐT: em Dương để được tư vấn ngay nhé.', 'AVAILABLE', 'Quận Bình Thạnh, Tp Hồ Chí Minh', 50, 11000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4e451fbc-a3d7-4429-8a74-5462083bd558', '4a612297-1d3a-492e-9971-0b2678e8373b', 'IMAGE', 'https://cdn.chotot.com/Fc_77eCHx9qbwQtTvzVprh7ovsEg47z1N8XIie2x-Hg/preset:view/plain/492be36d2d7cbd9aa98f97b4e6c40fec-2973910713032099003.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3ffd183f-30a9-4387-a080-7e3c6f6277c2', '4a612297-1d3a-492e-9971-0b2678e8373b', 'IMAGE', 'https://cdn.chotot.com/iHJvy7uAPFjxpu3bqFCGqr3KRj5-4x7-AM-KC_6hj4Y/preset:view/plain/a2d064c85896888f3bd033c34c1784c4-2973910712842896482.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('86ee2b1d-8260-4dc0-8948-c342d47facd4', '4a612297-1d3a-492e-9971-0b2678e8373b', 'IMAGE', 'https://cdn.chotot.com/Ok3gSmmQLNODoOUO3jVFzH0DF-5Ir-Hn7H7a42PNNgw/preset:view/plain/930489508fdb0b9647318e0cd1a6b784-2973910712858344492.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('224da3ab-4af2-4d8d-ac90-bc361113d401', '4a612297-1d3a-492e-9971-0b2678e8373b', 'IMAGE', 'https://cdn.chotot.com/bhUAFsxWB9y8RWNHOLMm8EHkzu0v-O4fyHrRdPYnSv4/preset:view/plain/402c9d3976f98323cb90a66eedff98b1-2973910712684963453.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('16b43635-c700-4bed-b6cc-34c2d1c323f0', '4a612297-1d3a-492e-9971-0b2678e8373b', 'IMAGE', 'https://cdn.chotot.com/f-aU_fVaZNx9D_31Pgk5ANjwYe36T96yofzUt6NNE1I/preset:view/plain/fd7b3382c5610eabfb6c2e00c72c85ac-2973910713250213362.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('60efb96e-960f-4504-91c9-3f8b7183cb68', '4a612297-1d3a-492e-9971-0b2678e8373b', 'IMAGE', 'https://cdn.chotot.com/cn1wtS8AGCuvbIkOCvZFwwPXA3C5EHNMuYHMMuuYrMU/preset:view/plain/8af6818dd36eb06a22b5821e22896ffa-2973910713199861783.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b7f7145f-e316-43f6-ac82-5eb604d54a05', '4a612297-1d3a-492e-9971-0b2678e8373b', 'IMAGE', 'https://cdn.chotot.com/GKku98I3QC3v98kDxJEQoUDmEnJrxldKltKJnTN5swE/preset:view/plain/e5813f7673b17330f8c45aab360b328a-2973910712858701306.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f85799cb-cd94-497c-9dee-07b7680e7870', '4a612297-1d3a-492e-9971-0b2678e8373b', 'IMAGE', 'https://cdn.chotot.com/HUhgvhFHPO4LZ9wjknu-vGZRge8mONJnMgflfPeu1dQ/preset:view/plain/15c6cad3090ad0ba2c85650ee8cf8c0b-2973910712874884178.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('74f740ed-9180-45a4-ad52-67658c585ce2', 'P_133940949', 'APARTMENT', 'Siêu phẩm căn hộ dịch vụ mới khai trương ngay kdc Kim Sơn, kế tdtu,…', 'Dự án: 
Thông tin chi tiết: 🎉 KHAI TRƯƠNG CĂN HỘ 1PN CAO CẤP – KDC KIM SƠN, QUẬN 7 🎉

🎁 ƯU ĐÃI ĐẶC BIỆT THÁNG 8: Giảm ngay 1.000.000đ cho khách check-in trong tháng 8!

📍 Vị trí đẹp KDC Kim Sơn, Quận 7 – gần Nguyễn Hữu Thọ, RMIT, ĐH Tôn Đức Thắng, Lotte Mart và Phú Mỹ Hưng
🛏️ Thiết kế 1 phòng ngủ riêng, không gian rộng rãi, sang trọng và cực kỳ thoáng mát
🌿 Cửa sổ lớn/ban công đón ánh sáng tự nhiên, không khí trong lành
🛋️ Full nội thất mới 100%: giường, sofa, TV, tủ quần áo, bàn ăn
🍳 Bếp hiện đại với tủ lạnh, bếp nấu, lò vi sóng, máy hút mùi
🧺 Máy giặt riêng – máy lạnh inverter – nước nóng lạnh đầy đủ
🏢 Tòa nhà mới an ninh, thẻ từ, camera giám sát, giữ xe
✨ Phù hợp người đi làm, cặp đôi, chuyên gia và khách nước ngoài', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 40, 7000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1941568c-1d97-454c-bc5c-11fb7d8a23ac', '74f740ed-9180-45a4-ad52-67658c585ce2', 'IMAGE', 'https://cdn.chotot.com/lFLxixoTYGJwD7B95TVV7cRgeEJIUFDrJoXjIlnxeNY/preset:view/plain/199b554ecd1e430786793de057cea445-2996122808401905124.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('95f5785f-cbb4-4618-b03f-595da4f4a360', '74f740ed-9180-45a4-ad52-67658c585ce2', 'IMAGE', 'https://cdn.chotot.com/T0y7JIEILgMfWU5X3uzKLhQPVf3QwI81foBLfqtAFLw/preset:view/plain/f943dfef35daaf6ef42454c6b1d651c9-2996122808508631417.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3590fe73-fd10-4795-bf65-ac378e98cc5e', '74f740ed-9180-45a4-ad52-67658c585ce2', 'IMAGE', 'https://cdn.chotot.com/bvJRHCV19jNG8bjMoR9LoQ5FE3PSQtg24-nbGIJWttE/preset:view/plain/ae9b62e7576fcb09bdf895a48ccefce9-2996122808555247769.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('135b6bf7-b6f0-40e8-9170-58214bb2e50b', '74f740ed-9180-45a4-ad52-67658c585ce2', 'IMAGE', 'https://cdn.chotot.com/XUgG67C4F-Sbl_CLvZR5cayaq1uSOI8ugHkvrPmbMvc/preset:view/plain/3bcb769947dbf5500b33355aa26e2ac6-2996122808607460967.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('3c771d04-f3b5-4f3b-b0cc-277a21161f33', 'P_133940948', 'APARTMENT', 'Cho Thuê Căn Hộ Studio Ban Công Full Nội Thất Cao Cấp Trung Tâm Quận 7', 'Dự án: 
Thông tin chi tiết: 🏡 CHO THUÊ CĂN HỘ STUDIO BAN CÔNG – FULL NỘI THẤT CAO CẤP | TRUNG TÂM QUẬN 7 ✨

📍 Đường Lý Phục Man, Phường Bình Thuận, Quận 7
Vị trí thuận tiện, dễ dàng di chuyển đến Phú Mỹ Hưng, Lotte Mart, TDTU, RMIT và các khu vực lân cận.

✨ THÔNG TIN CĂN HỘ:
▪️ Studio thiết kế hiện đại, không gian rộng rãi và riêng tư
▪️ Có ban công riêng thoáng mát, đón ánh sáng tự nhiên 🌿
▪️ Nội thất cao cấp, mới đẹp – chỉ cần mang vali vào ở 🧳
▪️ Giường, nệm, tủ quần áo
▪️ Máy lạnh, tủ lạnh, máy giặt
▪️ Bếp riêng tiện nghi, đầy đủ khu vực nấu ăn
▪️ Phòng sạch sẽ, sáng sủa, bố trí tối ưu không gian

🏢 TIỆN ÍCH TÒA NHÀ:
✅ Hầm để xe rộng rãi, tiện lợi 🛵
✅ Bảo vệ trực 24/7, an ninh và an toàn
✅ Thang máy hiện đại
✅ Camera giám sát khu vực chung
✅ Ra vào thuận tiện, môi trường sống văn minh
✅ Tòa nhà sạch sẽ, được quản lý chuyên nghiệp

📍 VỊ TRÍ THUẬN TIỆN:
🚗 Gần khu đô thị Phú Mỹ Hưng
🛍️ Dễ dàng di chuyển đến Lotte Mart Quận 7
🎓 Gần Đại học Tôn Đức Thắng (TDTU) và Đại học RMIT
☕ Xung quanh có nhiều quán cà phê, cửa hàng tiện lợi, siêu thị và khu ăn uống

💰 GIÁ THUÊ HẤP DẪN – LIÊN HỆ ĐỂ NHẬN THÔNG TIN CHI TIẾT!

📩 Inbox ngay để nhận hình ảnh, video thực tế và đặt lịch xem phòng miễn phí!

⚡ Căn hộ đẹp – vị trí trung tâm – tiện ích đầy đủ. Liên hệ sớm để chọn được căn phù hợp nhé!', 'SOLD', 'Quận 7, Tp Hồ Chí Minh', 39, 5600000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b5c7da29-0ddd-43d9-8e68-26df637d4276', '3c771d04-f3b5-4f3b-b0cc-277a21161f33', 'IMAGE', 'https://cdn.chotot.com/Y5j47GVkuzzOK73-2z_CjhSjEHzOQtq9Ta-C4yHM3n4/preset:view/plain/36fdaaaa94497c0fd7a3fabf5e327139-2996123296483523309.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('498e754d-3117-42de-a03a-7b73abbdd835', '3c771d04-f3b5-4f3b-b0cc-277a21161f33', 'IMAGE', 'https://cdn.chotot.com/p_eJiB2TpGrimdvYg9qQRrTMUENb9wHuCDQnbON6zOk/preset:view/plain/23143986ea85dddffd29ad47400f33ef-2996123296449579385.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('de27a520-09f9-444d-8b6b-8d3e5bd07bc5', '3c771d04-f3b5-4f3b-b0cc-277a21161f33', 'IMAGE', 'https://cdn.chotot.com/ltOOJvbMdLnC3_GtVwZvpdwB7sa9EUzSMw_dcnlRr4g/preset:view/plain/423cb1255d4da39c1202f9252c266fb9-2996123296525501924.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e8868442-e607-400e-994a-6a35e2230579', '3c771d04-f3b5-4f3b-b0cc-277a21161f33', 'IMAGE', 'https://cdn.chotot.com/dKvOd-EYohYG1TZdhWTxm4tijnBomH70Rgvh90Xo-D4/preset:view/plain/f6e720f290823623b0972c9f3487c44d-2996123296689651213.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a614bb34-2788-4f49-9c62-fd23ea405af8', '3c771d04-f3b5-4f3b-b0cc-277a21161f33', 'IMAGE', 'https://cdn.chotot.com/w2FYjOdi6ZR2bZoYS_qa7Agcw6VxHZ0MYCzJpWvUx3w/preset:view/plain/a175532ea5080ae0c4b6c42aaccd7ee2-2996123296962499583.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d122d6c1-a9a4-47dc-95da-9f1aa3665a52', '3c771d04-f3b5-4f3b-b0cc-277a21161f33', 'IMAGE', 'https://cdn.chotot.com/7XJSxfiX5hETJ5aY2aDmCTz2YtEnBN8SW4TrHXd-FRI/preset:view/plain/7abde9b368c8b2dd5974fd2331d99f55-2996123296594040985.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('53316725-526a-4eea-a5a3-189a6516c6bf', '3c771d04-f3b5-4f3b-b0cc-277a21161f33', 'IMAGE', 'https://cdn.chotot.com/3iDa0zZknDxOOPfdysO0yB2d56jyMtxDGI-N4C0OMEY/preset:view/plain/c6d88ec43a383d6d91f022cc74c44930-2996123296606348966.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('aa953220-dc05-41ea-840e-ca2917dd0218', '3c771d04-f3b5-4f3b-b0cc-277a21161f33', 'IMAGE', 'https://cdn.chotot.com/6f0aKSvzkpXW7YGSJw8qbVJeSNy8O_bH52kPPR4ZIfQ/preset:view/plain/99e29818e5b2e5abe12b9f56185a8b59-2996123296568419364.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0a786dc5-a088-49e8-9a6c-1d24c58cf472', '3c771d04-f3b5-4f3b-b0cc-277a21161f33', 'IMAGE', 'https://cdn.chotot.com/V8jS3sP5O6VZoJtKXyKlJsCIj8H7SpieRO_CSFuwzmM/preset:view/plain/cd240a16bf51a8652fcea15d31652c11-2996123296616483893.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('506beb34-8d7d-4e18-b9af-b067e815c46c', 'P_133220952', 'APARTMENT', '✅ Cho Thuê Căn Hộ_Ban Công_Thang Máy Hầm xe_Bảo Vệ_Nơ Trang Long✅', 'Dự án: 
Thông tin chi tiết: Hệ thống hơn 1000+ căn hộ khắp các quận chỉ chờ khách iu tới chốt.

✅Hà Dương luxury apartment✅
( Nhiệt tình, Uy tín, Trách nhiệm)
~~~~ ~~~~ ~~~~

✅VỊ TRÍ CĂN HỘ:  Đường Nơ Trang Long, p12 Bình Thạnh
- Cam kết hình thật + Giá thật
- Tiền cọc: 1 tháng tiền nhà
✅ Giá Phòng: 5,500,000✅

✅Giá Phòng bao gồm:✅
📢Dịch vụ tốt, chỉ cần xách vali vào ở.
📢Bảo Trì, Sửa chữa, Giờ giấc tự do, Hầm xe rộng rãi.
📢gần nhiều tiện ích, dọn vệ sinh thang máy, hành lang mỗi ngày.
📢Bảo vệ 24/7, an ninh tốt, dân cư yên tĩnh, văn minh. 
📢 Có Thang Máy, ra vào bằng vân tay
📢Full Nội Thất đầy đủ các thiết bị cần thiết….
      ...............
✅Ngoài ra, Dương còn cơ số căn hộ xịn xò khác ở Các Quận:
- Studio, duplex ban công, cửa sổ giá từ: 6tr9
- 1PN Đẹp giá từ: 10tr
- 2PN, Căn hộ cao cấp giá từ: 12tr

📲Inbox Dương hoặc liên hệ hotline / nhắn tin Zalo qua SĐT:em Dương để được tư vấn ngay nhé.', 'AVAILABLE', 'Quận Bình Thạnh, Tp Hồ Chí Minh', 35, 5500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('87ca59cb-d377-4552-93dd-75e472bf91f9', '506beb34-8d7d-4e18-b9af-b067e815c46c', 'IMAGE', 'https://cdn.chotot.com/sBiQ7IQnTkD0MBTwzY0I2x0DxRPvy6YQWbSPLNp6paE/preset:view/plain/58f8d27fe29b6f44b415aaf939ad383e-2990609847869981061.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('501cbcb5-c179-4c85-9cf8-05fbacdb027b', '506beb34-8d7d-4e18-b9af-b067e815c46c', 'IMAGE', 'https://cdn.chotot.com/2ixRFf2Srl_j2dvTxiOpw3FJtTOS3dPk1DqWOa9OzEU/preset:view/plain/c2e7cbb9624715cb4bef17b39847c1af-2990609847864092763.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e858dd86-974e-406f-9ade-e695b2afdb1f', '506beb34-8d7d-4e18-b9af-b067e815c46c', 'IMAGE', 'https://cdn.chotot.com/jkqThy3_qUJEhNvzi5oTi0ezn-OrgC-6H5Z93B9evZo/preset:view/plain/fe406255315786bec7087d722cc7565b-2990609847877834549.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7ef3adc3-dcca-46a6-bee5-a9aba59f3291', '506beb34-8d7d-4e18-b9af-b067e815c46c', 'IMAGE', 'https://cdn.chotot.com/i2MrM0_vYHTQAMPWjM5RLXLEfYn8eGqvLOgkF7hjkuI/preset:view/plain/692399768a58093581c795f4b1fc5a6c-2990609847902437834.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ebb1cc18-9c1f-4abc-968d-60194d9843dc', '506beb34-8d7d-4e18-b9af-b067e815c46c', 'IMAGE', 'https://cdn.chotot.com/BAWZe4gYxmIYHFKM40zFu_usIIX3m6ryLgfxrx5FZb4/preset:view/plain/327d14e99ce3cd30ba591b68e333cdff-2990609848338555722.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('36e7ccfb-12fb-494d-b650-744aab75f268', '506beb34-8d7d-4e18-b9af-b067e815c46c', 'IMAGE', 'https://cdn.chotot.com/x3E4jIVIiAWHiqcT0lkXT8MjTM8olafgTmCk-bvfqJY/preset:view/plain/ee90c70a7536a715a6e2482f21701c52-2990609847937139722.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('9bc5bcfd-e02c-4273-b11c-745b21ff38ef', 'P_131440332', 'APARTMENT', 'Bán căn hộ 2pn stown dt61m2 giá 3.5 tỷ', 'Bán căn hộ chung cư stown tham lương
căn hộ 2 phòng ngủ 2 vệ sinh
dt61m2 giá bán 3.5 tỷ 
căn hộ đã có sổ hồng
Vui lòng liên hệ!
#stownthamluong
#canhoquan12
#taidinhcu38ha
#canhothamluong', 'UNDER_OFFER', 'Quận 12, Tp Hồ Chí Minh', 61, 3500000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a3d01e2c-fd62-4c1d-ad53-0f24adc3dc25', '9bc5bcfd-e02c-4273-b11c-745b21ff38ef', 'IMAGE', 'https://cdn.chotot.com/d8HMLdD14U_fp2VirIboCx1xGymaMP4Z3awFyM16r0I/preset:view/plain/d45d1f8d092892bfc8bd2278f285552a-2977134461086535870.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0b227421-08b7-4648-beb4-391676637d1f', '9bc5bcfd-e02c-4273-b11c-745b21ff38ef', 'IMAGE', 'https://cdn.chotot.com/S4S6-8A1r3qqH10oRH8ldv_NzCirsGKeJtVcf0ugA70/preset:view/plain/786b83cfd7b4a02c806d7d0e0eb227ab-2977134461881806110.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('24f823b1-676d-46c9-953a-c2f9b8f01e24', '9bc5bcfd-e02c-4273-b11c-745b21ff38ef', 'IMAGE', 'https://cdn.chotot.com/lG_eBvlgMhKdhnMlxaqpn9IdayP1PO30o-YZRboyaSU/preset:view/plain/896af76130b428ca412ab6e61bff883c-2977134463794308654.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fe537c60-34ac-437d-804d-0f5a91a62606', '9bc5bcfd-e02c-4273-b11c-745b21ff38ef', 'IMAGE', 'https://cdn.chotot.com/hNiAS2C8iUZE7smv3gksaxx6MQKe65d3fijS-bvQgr0/preset:view/plain/fc5f86460531f3af2f698186bb464d82-2977134463290861102.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2bdfe360-cdc1-403d-a3db-ff856b613c32', '9bc5bcfd-e02c-4273-b11c-745b21ff38ef', 'IMAGE', 'https://cdn.chotot.com/W-S8QRL0NOXd99zimWxy-Iiyy-iGHv28Yf5GR-aFCm4/preset:view/plain/0375b2096cbd447561762611f9cf0c3e-2977134461176749732.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9c558cfd-c90a-4d9d-99ce-2ea1ba374bf8', '9bc5bcfd-e02c-4273-b11c-745b21ff38ef', 'IMAGE', 'https://cdn.chotot.com/F7OsO3AfnjRESDvB2rOxoNFxWyp23Ew5-pLs30FGSqY/preset:view/plain/b858de40444fabfa7167b6bb06b304ff-2977134461730291404.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1774e0c8-2090-4d77-b52e-6ef7ff0923b6', '9bc5bcfd-e02c-4273-b11c-745b21ff38ef', 'IMAGE', 'https://cdn.chotot.com/Kf3wPAwq81Wgm3sT8B3FayPuOZRn2WQLzG7fwnez7n8/preset:view/plain/242a197d8c08237167ce4e4048c9eab0-2977134461133730053.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('f5a0c47c-3967-4e28-8528-4f2f30f8f2b9', 'P_122919251', 'APARTMENT', '✅Hệ Thống Căn Hộ_Mới 100%_1PN 50m2_Nội Thất Cao Cấp_Bùi Đình Tuý✅', 'Hệ thống hơn 1000+ căn hộ khắp các quận chỉ chờ khách iu tới chốt.

✅Hà Dương luxury apartment✅
( Nhiệt tình, Uy tín, Trách nhiệm)
~~~~ ~~~~ ~~~~

✅VỊ TRÍ CĂN HỘ:  Đường Bùi Đình Tuý, Bình Thạnh
- Cam kết hình thật + Giá thật
- Tiền cọc: 1 tháng tiền nhà
✅ Giá Phòng: 10,000,000✅

✅Giá Phòng bao gồm:✅
📢Dịch vụ tốt, chỉ cần xách vali vào ở.
📢Bảo Trì, Sửa chữa, Giờ giấc tự do, Hầm xe rộng rãi.
📢gần nhiều tiện ích, dọn vệ sinh thang máy, hành lang mỗi ngày.
📢Bảo vệ 24/7, an ninh tốt, dân cư yên tĩnh, văn minh. 
📢 Có Thang Máy, ra vào bằng vân tay
📢Full Nội Thất đầy đủ các thiết bị cần thiết….
      ...............
✅Ngoài ra, Dương còn cơ số căn hộ xịn xò khác ở Các Quận:
- Studio, duplex ban công, cửa sổ giá từ: 6tr9
- 1PN Đẹp giá từ: 10tr
- 2PN, Căn hộ cao cấp giá từ: 12tr

📲Inbox Dương hoặc liên hệ hotline / nhắn tin Zalo qua SĐT trên để được tư vấn ngay nhé.', 'UNDER_OFFER', 'Quận Bình Thạnh, Tp Hồ Chí Minh', 50, 10000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d8b0add6-658f-40e7-b61e-2a2a827c4c83', 'f5a0c47c-3967-4e28-8528-4f2f30f8f2b9', 'IMAGE', 'https://cdn.chotot.com/-VLS86T7jYITPO4qQF-IORPCo0Y1ydkItugCpnhMfro/preset:view/plain/7348557b9315bc696056a1cc1fec4f84-2918970998676091646.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('faa188fa-b0e1-4dfa-a18e-05cea8a47e75', 'f5a0c47c-3967-4e28-8528-4f2f30f8f2b9', 'IMAGE', 'https://cdn.chotot.com/SkKEwJrcIN6bRyyVDs-fiLn0Cn12omddUVZ4jTA4zqE/preset:view/plain/fbbb7cac0ab77f3f5b0a7b68516074ea-2918970998342901953.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d7512f38-6e4b-4049-a8eb-2c7ac04d29af', 'f5a0c47c-3967-4e28-8528-4f2f30f8f2b9', 'IMAGE', 'https://cdn.chotot.com/g_xKGdXKnU3dxa7EvlSCHYVxEU1ZVqQfnYxO_Q8qH78/preset:view/plain/44cb8e7754b5fdd96ed820e7cc33418d-2918970998273399121.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b6386f7c-8bb1-41d5-b4c6-8bec6a6e2994', 'f5a0c47c-3967-4e28-8528-4f2f30f8f2b9', 'IMAGE', 'https://cdn.chotot.com/6vPHJWS5hF8fIBGIYT3AEcNGmmvnTJUxznqWkdnX8qY/preset:view/plain/e44b9cbe3c3b9bcb23d21aed8764055d-2918970998290778883.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dae24e22-ad1b-4543-ae2f-d0b2f93a683f', 'f5a0c47c-3967-4e28-8528-4f2f30f8f2b9', 'IMAGE', 'https://cdn.chotot.com/nqCYUVQQWYC3DZv2CycOVCWiSLaN1_b8xVzQBuMIPgc/preset:view/plain/377dfd4642776043fe00f192fd28fab3-2918970998266565274.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2326fa6d-2fcd-4fb8-801d-5d116a93d200', 'f5a0c47c-3967-4e28-8528-4f2f30f8f2b9', 'IMAGE', 'https://cdn.chotot.com/iYMf_eCYLZZ3Y02PMEHIUaYpSNwi9KHc9XWs0jLxBS8/preset:view/plain/64a2db882f54647aba01931325a7a6fa-2918970998422747021.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f9408e27-e134-43da-9389-2a53a51d77ff', 'f5a0c47c-3967-4e28-8528-4f2f30f8f2b9', 'IMAGE', 'https://cdn.chotot.com/RMvj11mwwU4RCTBWCruV62_Z1okH2J-jzg3vt0p-Txw/preset:view/plain/b2467f6e4fe92a3e68af99807d155219-2918970998377739049.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2e1741b0-afe5-4379-87b0-885ff64f8983', 'f5a0c47c-3967-4e28-8528-4f2f30f8f2b9', 'IMAGE', 'https://cdn.chotot.com/mF7VynZRW-ibAdNmKzvxvE25epZRWOf5bOurP7EAmuM/preset:view/plain/0de59e794d516f90604d023b49f81ffc-2918970999582690051.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('13e6be09-2829-4636-8222-6419672bd7ab', 'P_133677846', 'APARTMENT', 'Căn hộ full nội thất 1PN - 1PK tách bếp khu sân bay TSN, quận Tân Bình', 'Dự án: 
Thông tin chi tiết: CAM KẾT ẢNH THẬT - GIÁ THẬT 100%
Chính chủ cho thuê
Nhà đầy đủ nội thất 1PN - 1PK tách bếp ngay Sân bay Tân Sơn Nhất (cách 1p di chuyển)
Nhà có thang máy - free giặt sấy ...
Tách bếp - cửa sổ ban công lớn thoáng mát ...
Ngay Bạch Đằng - Lam Sơn - Hồng Hà , P2 , Tân Bình
Thuận tiện di chuyển các quận Gò Vấp , Phú Nhuận , Tân Phú ...
Diện tích: 50m2
Kết cấu: đầy đủ nội thất cơ bản , free máy giặt - sấy
Giá (Cực tốt) : 6tr8
----------------
Liên hệ mình hỗ trợ SĐT (Zalo) : Đạt Đạt', 'SOLD', 'Quận Tân Bình, Tp Hồ Chí Minh', 50, 6800000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4b1975bc-0863-4780-8ef1-5419a1f63d17', '13e6be09-2829-4636-8222-6419672bd7ab', 'IMAGE', 'https://cdn.chotot.com/5gq73z0tbyMO-PSuUMTIvL_cN5A5FeAYnJbq7C8AFY8/preset:view/plain/3aedd7ff7803fcbf038befaca5ad5e12-2994109171968113855.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3450c825-9922-4d3c-a5d7-dff211c29fb9', '13e6be09-2829-4636-8222-6419672bd7ab', 'IMAGE', 'https://cdn.chotot.com/IK2KyYF4M19uzhAya7REyla_rKPZRH1rXOCZa-GsSJY/preset:view/plain/db926c1c82c6fd41b12b7f1c5be49a69-2994109173273063864.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('49916622-cb0d-4534-ba1c-c8a4b504a0dd', '13e6be09-2829-4636-8222-6419672bd7ab', 'IMAGE', 'https://cdn.chotot.com/VPauYHJIX686My6G70Y9WTyMX2jvhwkWyhFrWVvkGbQ/preset:view/plain/a65852de6f9c6341b3958f68e2302de2-2994109174336080887.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('013b06f3-75ad-442d-a611-811bd0d81671', '13e6be09-2829-4636-8222-6419672bd7ab', 'IMAGE', 'https://cdn.chotot.com/-sYFnYD6EUwBSA6Y7fnmhCT_qJLkNplv_DI8uOtVD3Y/preset:view/plain/20b949963d304b03400efd5a186b3637-2994109177919136594.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bafee5ad-128e-4b98-a473-4c4c563fd589', '13e6be09-2829-4636-8222-6419672bd7ab', 'IMAGE', 'https://cdn.chotot.com/Yttq-sY97mkIZpr546qM_CuRRuj49s7it6LiywwhFJ4/preset:view/plain/b6f28b5686299cffdfc31e8004015e06-2994109175859337414.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a9cc16e0-77df-4fe7-bbc1-f5793037c9dd', '13e6be09-2829-4636-8222-6419672bd7ab', 'IMAGE', 'https://cdn.chotot.com/JyDHYRWQAD-R8KI2rZcxnxnQaJT8z6SuxzVdCThZrz4/preset:view/plain/925500ab3de289761548c0ca72e7f753-2994109176292213919.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ca1be0f3-a498-46a4-95ba-64fec688a1bd', '13e6be09-2829-4636-8222-6419672bd7ab', 'IMAGE', 'https://cdn.chotot.com/6PDUZzXssWaB1cp42tyBCVBdrBw784HONmv5-fZ08No/preset:view/plain/7589af12542ed913b3f7d9b74a30dfbd-2994109171919902185.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6f7e996c-10f8-4960-98d6-dc76c670c438', '13e6be09-2829-4636-8222-6419672bd7ab', 'IMAGE', 'https://cdn.chotot.com/UREhTE-Mmo01uoIQNbOni7k2d2V89PYcxtyzeHhO7tY/preset:view/plain/3bc38a4854c689f9bf0611e1591914b2-2994109171458172840.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7dcb76ec-4e07-48c9-a700-9759e66f3408', '13e6be09-2829-4636-8222-6419672bd7ab', 'IMAGE', 'https://cdn.chotot.com/4EY7pDHDJCGPq5NM9MUYuX8przHrGI1pXuaiNhM9aGw/preset:view/plain/e43e895a6d9be6921cf1d5aeef1ba2c8-2994109172456516838.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('66fcb72d-7ec4-41cd-9a7c-b3d026279a48', '13e6be09-2829-4636-8222-6419672bd7ab', 'IMAGE', 'https://cdn.chotot.com/tqk0xmGZ8Fl1O-gJ-61FaIh4lcI7v6QKbdsQHR6Fx1s/preset:view/plain/02b5ee7334f606c07e501952a0600fd1-2994109171523493407.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('efaee39f-a9f9-49d4-b17d-0359a481a73b', '13e6be09-2829-4636-8222-6419672bd7ab', 'IMAGE', 'https://cdn.chotot.com/W0SrXcO_Q4CQBwCq5kcSklNkbyfYrxIsXt5v39NnPuI/preset:view/plain/f2742f1e88efe88f6361849f372ccaf0-2994109171751835791.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('37a3fcdd-88b2-4559-86f2-4b4fb48c5d08', '13e6be09-2829-4636-8222-6419672bd7ab', 'IMAGE', 'https://cdn.chotot.com/erFfN4WyZXTl3GKK4ZAYddU6lkI5PB1eDN3fO-6UYzg/preset:view/plain/fb40e9cac85a50c58657adb5cbb0f1db-2994109172177443466.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('88f65d6e-ce78-43be-8a43-350220f5c7fc', 'P_132736866', 'APARTMENT', 'Giảm sâu bán 2PN The Manor, 98m2, view thoáng mát', 'Dự án: 
Thông tin chi tiết: 🔥 Hàng hót 2PN The Manor
Căn hộ 2PN rộng 98m2, view nhìn ra ga Metro Văn Thánh, full nội thất 
💲 Giá chỉ 8.3 tỷ bao thuế phí, nhà đã có sổ. Còn thương lượng
- Sẵn hợp đồng thuê 24tr/ tháng
☎️ *** Liên hệ chốt ngay kẻo lỡ ạ', 'AVAILABLE', 'Quận Bình Thạnh, Tp Hồ Chí Minh', 98, 8300000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3988c658-d8f5-405c-9f57-99a081cc226c', '88f65d6e-ce78-43be-8a43-350220f5c7fc', 'IMAGE', 'https://cdn.chotot.com/QmRpyqctyysr5qhgjJQWxhrwJrx8S9wrtnPE72n3VGU/preset:view/plain/9e81444b2ec8ad9a1c1df14c43d63042-2986964162449857288.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cf3ec08c-8a8a-4302-b25a-fd2756938c11', '88f65d6e-ce78-43be-8a43-350220f5c7fc', 'IMAGE', 'https://cdn.chotot.com/OdCAofSfkQxpXSBsJHbo-WdCXI_fVJa4hzPePR4c4TA/preset:view/plain/7c6071a7a682c019b6f8a13953986f28-2986964162651924763.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e4f0f261-8b2a-4d48-871c-51832be2e759', '88f65d6e-ce78-43be-8a43-350220f5c7fc', 'IMAGE', 'https://cdn.chotot.com/rDb5L5ENusf16aIxIt-0lhQNlrHXPcG691PoG-dFQRo/preset:view/plain/b1240151533405f0b04eb299ae4a15e6-2986964163484061789.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7557298f-b661-47c9-8a95-c801bb9379d4', '88f65d6e-ce78-43be-8a43-350220f5c7fc', 'IMAGE', 'https://cdn.chotot.com/R2QRvYoDFoF2JitLwXf39ZT1D-pKBN7oTrXwO7kqzqE/preset:view/plain/3e387e1d06477dd564be9795299a226f-2986964162361997415.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('28f34774-5201-4e5c-8715-0fcb5cfdc728', '88f65d6e-ce78-43be-8a43-350220f5c7fc', 'IMAGE', 'https://cdn.chotot.com/-fxGXGMtMJPhmnF7GPGJu9ZQrChePRhWQFpRBeyVTGc/preset:view/plain/c0ecfb5ca97416ef8d8ae5ab49ce516e-2986964162443244611.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('20d6ce29-243e-4411-9a3b-a85a2cb79b5c', '88f65d6e-ce78-43be-8a43-350220f5c7fc', 'IMAGE', 'https://cdn.chotot.com/c6Ybq02dCAkdK5ai-Iy3TtAOrlSwb6yAr75OwwkDi0M/preset:view/plain/b743aa11101b9b17bef7838d0532c6e2-2986964163580064257.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('26c896d2-ca8a-4b39-8a85-14f784aa908b', '88f65d6e-ce78-43be-8a43-350220f5c7fc', 'IMAGE', 'https://cdn.chotot.com/KjjhJntF7VCv2MO6ezvqqz7f8NXdA43WGC-8CB5wthw/preset:view/plain/3cba0f56e6dea559d3cdcb853eafaf40-2986964163852596291.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bbebbfc9-d37a-4ed1-a898-abd9373c579e', '88f65d6e-ce78-43be-8a43-350220f5c7fc', 'IMAGE', 'https://cdn.chotot.com/CwvpE_L5Y19vhi40ddaqYBFgjoFMUUYI1YzspWMFRko/preset:view/plain/7370c314d6780c909e13c2a94cc76ecf-2986964163666559085.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bdb5e370-31c4-4c27-beca-5f99f3e499e6', '88f65d6e-ce78-43be-8a43-350220f5c7fc', 'IMAGE', 'https://cdn.chotot.com/eHTAu1Z85YvWPvUYN5TS44lZmkIwGXWzsTtLywISlBI/preset:view/plain/556ca02b2f883524d7ff2e4f416153ca-2986964163754571879.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('cad8ce3e-cdf8-4be3-978a-5990fd8c10db', 'P_123710081', 'APARTMENT', 'Studio SIÊU ĐẸP ngay KCN TÂN BÌNH_PHẠM VĂN BẠCH', 'Siêu phẩm mới tinh ngay PHẠM VĂN BẠCH_ KHU CÔNG NGHIỆP TÂN BÌNH( tiện ra các quận )

Hình thật giá thật 100%

👉🏻Thêm bớt nội thất tuỳ ý 
👉🏻 giấc tự do
👉🏻An ninh 24/7
👉🏻Được nuôi pet
👉🏻Chỉ tính thêm tiền điện nước

☎️Sms/ Nhắn tin / Call  để được xem phòng trực tiếp', 'AVAILABLE', 'Quận Tân Bình, Tp Hồ Chí Minh', 40, 4300000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('384dce9a-0dc3-43e3-bef9-f363d8f6a05d', 'cad8ce3e-cdf8-4be3-978a-5990fd8c10db', 'IMAGE', 'https://cdn.chotot.com/4lQ01Ng-vH-dir95eNlwizmBbW-DSQnKAuJJXl5L5kw/preset:view/plain/d15d6bec11138b4e6acf716fb758931b-2923405824053752642.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9ce5f844-3354-45b2-922c-84e83769c061', 'cad8ce3e-cdf8-4be3-978a-5990fd8c10db', 'IMAGE', 'https://cdn.chotot.com/rWNv8OsjaOwcyNvbo0RhK5M2WyYow1E7ASD243Sr4Jw/preset:view/plain/a3e65e8cce1921443e5fc3a3765b8ef0-2923405824005743181.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('edb867b2-06fe-45a0-9f8d-6176fcf3e874', 'cad8ce3e-cdf8-4be3-978a-5990fd8c10db', 'IMAGE', 'https://cdn.chotot.com/eJoBKf3Hi3bji58QrAsMZB5FV3uNqCGLiL6mb4VQXus/preset:view/plain/1ff83e4b46433cce46a516fe3d5a8084-2923405824036556394.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f8647129-95c1-4971-b13b-a0cce2052e2e', 'cad8ce3e-cdf8-4be3-978a-5990fd8c10db', 'IMAGE', 'https://cdn.chotot.com/ASgN3-BuXkh8plkhG0Y2D25dERRU9zqzYUvqYS5_RI0/preset:view/plain/34a98531b3d0120249e07eac4c3817db-2923405824143367042.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2f98f65f-628c-4bf1-bf7a-630613a860c3', 'cad8ce3e-cdf8-4be3-978a-5990fd8c10db', 'IMAGE', 'https://cdn.chotot.com/BOukQH--6BFoBKVmY8BHZnvnskTzPiAZu7VvJy8Jn7s/preset:view/plain/0b0f8af72de08abb407d0151062949e4-2923405824169979434.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a13544c8-c18f-4855-ad9f-d1fcea16ad8d', 'cad8ce3e-cdf8-4be3-978a-5990fd8c10db', 'IMAGE', 'https://cdn.chotot.com/fWiFFziAWoLJKhaxu-twcgnVFGASn6BlC2FEa-aspgU/preset:view/plain/7c7cf25c514ea40b91775241e10a3117-2923405824333861261.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e0ad3d52-dcda-427c-b35a-acdc0a851690', 'cad8ce3e-cdf8-4be3-978a-5990fd8c10db', 'IMAGE', 'https://cdn.chotot.com/q0m4dJ91xzkRD-c5YtOiwzJ4KVtZuYWXTk7E_9w8tBQ/preset:view/plain/a23ff584e8cb50c9e809f18a73e5342b-2923405824147428061.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('ebd5ffb3-ec9c-4aa4-bad7-e5e28d72523d', 'P_133940914', 'APARTMENT', 'CĂN HỘ 2PN BANCOL DƯƠNG QUẢNG HÀM FULL NỘI THẤT ĐẦY ĐỦ TIỆN ÍCH', 'Dự án: 
Thông tin chi tiết: 📌 364 Dương Quảng Hàm Gò Vấp 

- Diện tích 40m2 –  2 PN cửa sổ - Ở 3 người 
- Nhận xe ĐIỆN ( ko sạc hầm xe ) – Ko nuôi PET
- Điện : 4k – Nước 100k/người – DV 200k/phòng
- Giá 10.500.000 – Cọc 1 tháng – Ko nhận khách nước ngoài.', 'SOLD', 'Quận Gò Vấp, Tp Hồ Chí Minh', 40, 10500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c77a45d7-335d-4043-893c-f231b9cdfc09', 'ebd5ffb3-ec9c-4aa4-bad7-e5e28d72523d', 'IMAGE', 'https://cdn.chotot.com/uNDi3ChEbai_-hy2oE1FucjPyxSm4tMAfH15WQkgLMw/preset:view/plain/425b746fbcae12f4c94e35a85c6f7eb5-2996122983881657959.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('abbad54a-f649-4631-a9da-28b1a5c09758', 'ebd5ffb3-ec9c-4aa4-bad7-e5e28d72523d', 'IMAGE', 'https://cdn.chotot.com/LnizK5_2kSsJX04rmy9RbBnDuXpZnSg71SDoZw7CX2Q/preset:view/plain/086dbfcfa0692bfdbf7b8c7d6e73b865-2996122983861044708.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3ca3ea17-1b74-4a0b-a32d-f6dc8f5d7c1c', 'ebd5ffb3-ec9c-4aa4-bad7-e5e28d72523d', 'IMAGE', 'https://cdn.chotot.com/_zE2yQ6Exk41ZcnNjTCUCBSm868R6Cw5_oQycdkyigY/preset:view/plain/cfaa6ef2997b39981b4effe66e4fda78-2996122983934937465.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('745b9f0f-7453-4019-945f-d32940bbbb38', 'ebd5ffb3-ec9c-4aa4-bad7-e5e28d72523d', 'IMAGE', 'https://cdn.chotot.com/3-4o3QFNDWRPyBrSPxurE9SPQSPQMTO3IfB1Fjk8z70/preset:view/plain/337af3d760710ee9a4c2412c0cf47c9d-2996122983929911449.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('85072414-dec4-4d3c-82eb-7d4e173b764f', 'ebd5ffb3-ec9c-4aa4-bad7-e5e28d72523d', 'IMAGE', 'https://cdn.chotot.com/gPiS23BC8P1eK_Xx9iayeBSm-17_73eUxo8Tw1h0UnY/preset:view/plain/8980f72d47f56f9ba5e56d9a7132fbd4-2996122984057220699.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7d7664c7-abae-44b1-a753-88440f70508e', 'ebd5ffb3-ec9c-4aa4-bad7-e5e28d72523d', 'IMAGE', 'https://cdn.chotot.com/j0mO9KWiuebQ-VrVVjCzyJfv1uNgUmeNS34xqCP-wxo/preset:view/plain/ad4a1236c47b113df900489183a7ef41-2996122984048481279.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('772e4d75-bdc3-4449-852e-5e74682c8815', 'ebd5ffb3-ec9c-4aa4-bad7-e5e28d72523d', 'IMAGE', 'https://cdn.chotot.com/dE8nUK9OD4mTiUVbys5VS1_ki0i4TZtu-wfP_DQO6s4/preset:view/plain/63140b868cbd86c4d1ded5ce662882fd-2996122984020844632.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7829b3a0-e83a-439a-9411-387071a69e42', 'ebd5ffb3-ec9c-4aa4-bad7-e5e28d72523d', 'IMAGE', 'https://cdn.chotot.com/axbrbhUgMtvNIS87E6AayxcWwR2_d2jMU-_s4-yHmJg/preset:view/plain/5c604f38bf4846a08c2ae10d41d7db9f-2996122984117213265.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2cf1b04e-aebc-4734-9542-5ca96b41f573', 'ebd5ffb3-ec9c-4aa4-bad7-e5e28d72523d', 'IMAGE', 'https://cdn.chotot.com/9lgmEf60ZPp3np_XolL1DHpOC8-_ySOtxVDMSq55EXw/preset:view/plain/69246af0686f052fe2b41fc1a61cd815-2996122984038415085.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('45648705-7702-4256-b5d6-5e9882b490ab', 'P_133940912', 'APARTMENT', '🔴GIỎ HÀNG CHO THUÊ CH GIAI VIỆT🍀3PN2WC 150M💥NHÀ TRỐNG Ở NGAY👉VIEW ĐẸP', 'Dự án: 
Thông tin chi tiết: 🟢CHO THUÊ CH GIAI VIỆT
👉3PN 2WC 150M
👉NHÀ TRỐNG CÓ RÈM VÀ TỦ QUẦN ÁO
👉NHẬN NHÀ Ở NGAY
👉GIÁ THUÊ: 15TR/THÁNG
👉CÓ THỂ THÊM VÀO NỘI THẤT CƠ BẢN NẾU KHÁCH CÓ YÊU CẦU
——————————-
📍 Vị trí đắc địa: Toạ lạc tại số 854 - 856 Tạ Quang Bửu, Phường Chánh Hưng, TP.HCM. Trực thuộc Khu trung tâm hành chính. 
🩵Giao thông thuận tiện kết nối nhanh về các khu vực trung tâm lân cận trung tâm.
🌳 Tiện ích Công viên cây xanh, hồ bơi, phòng gym, khu BBQ, khu vận động thể thao.
🌆Trung tâm thương mại CenTral Mall 6 tầng đặt tại khu căn hộ thuận tiện vui chơi mua sắm.
🛒 Nhiều siêu thị, cửa hàng ăn uống, cửa hàng tiện lợi ngay dưới căn hộ. Gần các chợ, trường học, bệnh viện, ngân hàng.
🚘Hầm bãi đậu xe rộng rãi. Có chỗ đỗ ô tô
🔐Chất lượng quản lý tốt. An ninh khép kín 24/7', 'SOLD', 'Quận 8, Tp Hồ Chí Minh', 150, 15000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('876d7932-8669-4dc6-ad64-e01ad6dcf423', '45648705-7702-4256-b5d6-5e9882b490ab', 'IMAGE', 'https://cdn.chotot.com/lqstfGwfhPzUqWYD2eQqmTXkiImUcvZunJMiLxukjOM/preset:view/plain/dbfbcc71959255af791a67fdc96719ca-2996122972271562343.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('60f7ee8a-84e5-4e12-b270-7f1cb1168bf0', '45648705-7702-4256-b5d6-5e9882b490ab', 'IMAGE', 'https://cdn.chotot.com/AWf7Kcn7w9hmmGrIQR5bdJdWhgNfBXCRw6VkUvYFYp4/preset:view/plain/e65b212855d7c8058ae9590af0127c0a-2996122972022851961.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dcfd9850-1246-44b3-b956-6ef924424d9f', '45648705-7702-4256-b5d6-5e9882b490ab', 'IMAGE', 'https://cdn.chotot.com/sJOdBpNjB7AEg4hx5uiA285j04DGMTKZZ4nSh4fG7mY/preset:view/plain/ac2ce4d3b73b4dd4f8609fa80387fea5-2996122972571474073.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9c037922-feee-4585-b729-b26c41d3eaa3', '45648705-7702-4256-b5d6-5e9882b490ab', 'IMAGE', 'https://cdn.chotot.com/58HKvjDIup-0VIw8CZLkoYWjsGPsU5yHFA6ul3Fb7U4/preset:view/plain/e9d0ee6a1ab8a87fe5277d2fd64fa44f-2996122972284437988.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2a101d11-5d35-4635-8d62-0559bdd9f1a1', '45648705-7702-4256-b5d6-5e9882b490ab', 'IMAGE', 'https://cdn.chotot.com/BgzEXeJoSY0haT4wNdaanJH8xXMV2kLXQRFGg1DQ9E0/preset:view/plain/7b9db914c8bd73a49ce385e892c7cc1c-2996122973402098858.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2d062a03-bcb0-441c-9b10-c782d36d9077', '45648705-7702-4256-b5d6-5e9882b490ab', 'IMAGE', 'https://cdn.chotot.com/dhbU_DwYFz7cKn6aVNW_C39ixw-17J84L95KRn5Rwto/preset:view/plain/f5f6a326d9add4a5d25528ef4cf25828-2996122972511608920.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d0fb4da1-6f25-4bcf-a8dc-b62957a3f27f', '45648705-7702-4256-b5d6-5e9882b490ab', 'IMAGE', 'https://cdn.chotot.com/YUyJBHDSETBwgppV7Q99xMomjsu_7snja9jdzxMa1ig/preset:view/plain/bd25cef0a4c5e96791d91a6d9041d11d-2996122972582683684.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5d9f9b64-9391-4f57-951e-6a2a6808ef2f', '45648705-7702-4256-b5d6-5e9882b490ab', 'IMAGE', 'https://cdn.chotot.com/kGxIzkpL4_3uZAq6mXWJqE9TU_ja90T54_GdsktOd0M/preset:view/plain/c59a799cac79cc705f8d72a7ab8c2c7e-2996122973143159807.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('78124fff-0f74-49d4-a761-fb323c93dbfb', '45648705-7702-4256-b5d6-5e9882b490ab', 'IMAGE', 'https://cdn.chotot.com/VyQJci5QIjGbyOzR5_HAAPGEG5gPGRfS-j-KoQvUYU4/preset:view/plain/dd13cd3dfd8aa794a8debd9f035573d4-2996122972732534363.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c7b72ec2-bf8c-4252-ae09-bd50374957eb', '45648705-7702-4256-b5d6-5e9882b490ab', 'IMAGE', 'https://cdn.chotot.com/HQPSqWMkltn_XY4-dZsLtZ0pcX7ZQxRDg5eMQaP34SM/preset:view/plain/4d99da329dec0301dccce0cec598ae65-2996122973614610513.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3dc2a967-f9d3-49b4-bdbc-461f22d8524b', '45648705-7702-4256-b5d6-5e9882b490ab', 'IMAGE', 'https://cdn.chotot.com/XY0Ig2XBYYRk5FwQ8fXLVr_2No8xTDIHqmkBGUckW9Y/preset:view/plain/b902cc6110147e501bc76ebc6f5c6a98-2996122973855568903.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bf833188-0338-480b-a149-e621e16b8884', '45648705-7702-4256-b5d6-5e9882b490ab', 'IMAGE', 'https://cdn.chotot.com/pGWGyyxIiEzXm04eQYmU8wgldYVa7r0gVGr-BIr2j6k/preset:view/plain/57b4dce93e27081ed357d97a949a2b17-2996122973267833990.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('f466230b-c0a7-435e-ac72-4120b855b95e', 'P_133393418', 'APARTMENT', 'CHO THUÊ CHDV DUPLEX Q7 GẦN LOTTE, TDTU, RMIT, UFM 5P QUA Q4,1,8', 'Thông tin chi tiết: Cho thuê CHDV Duplex Ban công trung tâm Quận 7 có ban công, cửa sổ siêu lớn, thoáng VIEW TRIỆU ĐÔ, MÁY GIẶT RIÊNG

• Gần Lotte Mart, GO!, Phú Mỹ Hưng và Crescent Mall
• 5 phút qua Quận 4, Quận 8
• 10 phút di chuyển đến Quận 1
• Xung quanh đầy đủ quán ăn, cafe, cửa hàng tiện lợi, gym
• Toà nhà an ninh, khu vực yên tĩnh, giờ giấc tự do
• Ra vào vân tay/thẻ từ

Phù hợp người đi làm, nhóm bạn, cặp đôi hoặc khách thuê lâu dài cần không gian sống tiện nghi và thuận tiện di chuyển.

Zalo/WhatsApp: *** (Jonathan - Huy Tran)
ĐỒNG HÀNH CÙNG BẠN TRONG QUÁ TRÌNH "TÌM - THUÊ - Ở"

#canhoquan7dep #chothuecanhoq7 #studioquan7
#canholpnquan7 #fullntquan7 #canhogiarequan7 #canhomoiquan7 #canhodep #canhothangmay #canhobancong #phongtrodepquan7 #canhochinchu #canhoganquan7 #canhotiennghi #canhoganquan1
#canhoq7viewdep #canhodichvuquan7 #canhohimlamdep #canhogandaytienich #canhoquan7fullnt #chothuecanhodichvu #troquan7 #thuephongtro #chothuenhatroganTDTU #chothuecanhominiganUFM #chothuecanhominiganTDTU #chothuenhatroganUFM #chothuecanhodichvuganLotteMart #chothuecanhodichvuganCauTanThuan #chothuenhatroganLotteMart #chothuecanhomini #chothuenhatrophongtro', 'UNDER_OFFER', 'Quận 7, Tp Hồ Chí Minh', 40, 6000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e2ba7ce4-7c50-4ab3-80fb-6ab601642065', 'f466230b-c0a7-435e-ac72-4120b855b95e', 'IMAGE', 'https://cdn.chotot.com/V18tvZf7uiZgFjfRARRQGu_6ZPucld9oDE7g8GheLvI/preset:view/plain/74701e9bd1005422d38726446a6d27da-2994375144849985148.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9cfed276-ff50-4894-a259-78d0d7981f70', 'f466230b-c0a7-435e-ac72-4120b855b95e', 'IMAGE', 'https://cdn.chotot.com/-3EqIrUqGM8s31DYs2nSNJdOPX5_xdhz8ITTN3NGO1U/preset:view/plain/30649bbeb48772e1fd803715245db58e-2994375144936315797.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0d4176de-e00c-4af1-8974-522fbbfeeddc', 'f466230b-c0a7-435e-ac72-4120b855b95e', 'IMAGE', 'https://cdn.chotot.com/ODgbd5GiEwSHvbDBzhRjxgXOnsqx50l2Duabox8XBy0/preset:view/plain/b3dd47cfefb122496c147c44d3092db5-2994375145030313093.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a1f661bd-a194-4f89-b96a-d78c63dec9aa', 'f466230b-c0a7-435e-ac72-4120b855b95e', 'IMAGE', 'https://cdn.chotot.com/XyYM4Hmq_DD0GSxHdB9iBlUGJzv_ct8pd3nlPtQthaM/preset:view/plain/0fc7f0e31013bb2fb7e1e6df2c870b24-2994375144562026408.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2ba81b39-7823-460a-bad0-d64bf4acec13', 'f466230b-c0a7-435e-ac72-4120b855b95e', 'IMAGE', 'https://cdn.chotot.com/MZq-_Xg-W24hKAlHhkd7spMGYPyjCol5dsm_XSBarrg/preset:view/plain/926ab45ef230bd2e4d996ed57ebb072d-2991930672652294308.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('974d2311-a5ab-412a-848d-b86eec14d4db', 'f466230b-c0a7-435e-ac72-4120b855b95e', 'IMAGE', 'https://cdn.chotot.com/rmV68CyAl3xGLR5Qr_t0ykk6w5HxpbV0ar5KyAHwKXw/preset:view/plain/a3612ea40533145fa9adce78132e11f8-2991930681947068580.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7d45f00a-db71-4832-834c-81c3ef47a484', 'f466230b-c0a7-435e-ac72-4120b855b95e', 'IMAGE', 'https://cdn.chotot.com/tW-uG41bywQk4JZxcosVF5dW2z3QF_09iKRykk8-kMI/preset:view/plain/51bb63316706dea8e40c4db9f2644278-2991930695683793273.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('24788222-5390-4969-a09f-438ad59e8f24', 'f466230b-c0a7-435e-ac72-4120b855b95e', 'IMAGE', 'https://cdn.chotot.com/gzxnGb4zH2Dj3a7b-uOa2uB0MCcfB1-uelOiZpxpWUg/preset:view/plain/4e764da8474575c38efc0c7e3ca5c5fd-2991930701895930360.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7f6a4f61-81c9-420a-8df7-520b51b3f984', 'f466230b-c0a7-435e-ac72-4120b855b95e', 'IMAGE', 'https://cdn.chotot.com/rlQ2Ll0i47aql2Kic6eXBjTsBKzUqNAQoQ3QtNxsPKU/preset:view/plain/95566cf282e95c8129908610741fb51f-2991930755130792100.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('85578753-4003-4eb3-b7b0-0a1d65509c88', 'f466230b-c0a7-435e-ac72-4120b855b95e', 'IMAGE', 'https://cdn.chotot.com/oKOZHvtCOPAU8rXQaZXVRVv-fcKyevYZZhgaRQPF8JA/preset:view/plain/a25e16908ed5d35cc2d72a283d601fa1-2991930775146631672.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('780c1097-5224-4363-a616-ee9a1209778a', 'f466230b-c0a7-435e-ac72-4120b855b95e', 'IMAGE', 'https://cdn.chotot.com/g9lVKsW0v3VBvscyGnB7bRGc35mWw_jOXaLV4ixcuWk/preset:view/plain/cc8fb8e863160fc3f491ea57ae9398fd-2991930792712804516.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('aa505059-7e4b-418d-91ca-5c90011155fa', 'f466230b-c0a7-435e-ac72-4120b855b95e', 'IMAGE', 'https://cdn.chotot.com/Xh6NAyzjbDMMxfI3oSAkaDZ7RyMQkyLQE48paCfMmXU/preset:view/plain/9964d6279bd281a58011463a5b4fe161-2991930803713200961.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('325a356f-fb87-4b1a-b270-b0069fa4c6a8', 'P_131056734', 'APARTMENT', 'Duplex mới khai trương sát lotte mart TDT , RMIT', 'Khai Trương Dự Án Tại 30 Lâm Văn Bền Quận 7


!! Nội thất gồm: Máy lạnh, tủ lạnh, tivi, bếp điện, máy giặt, sofa, bàn ,lò vi sóng,máy nóng lanh, tủ quần áo
⛔  Khách không lấy tv có thể thương lượng giảm giá

!!! Phí dịch vụ
- Điện: 4k/kWh
- Nước: 100k/ng
- Xe: 100k/xe
- Quản lý: 200k/phòng', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 35, 5500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('53bd8729-f3c3-447f-8d94-ec9949066483', '325a356f-fb87-4b1a-b270-b0069fa4c6a8', 'IMAGE', 'https://cdn.chotot.com/4n9n0_oHj7IWuuTrqSxR-q3SchWE0c5TLooKDD6X1Xc/preset:view/plain/0f1fe817d6766c3dd62f1849fcf8b306-2974401836731894168.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f53320aa-5762-4a38-92af-4ba322b6b10c', '325a356f-fb87-4b1a-b270-b0069fa4c6a8', 'IMAGE', 'https://cdn.chotot.com/Y2SmUZ_pmuCq-MGKLqKrwr2v_16cnv-EpzlJbktGO3U/preset:view/plain/f4a283c337470d9daebdd8dab3d1feea-2974401837087564294.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('47eb84e0-86c2-4981-a49e-0c377ae2f754', '325a356f-fb87-4b1a-b270-b0069fa4c6a8', 'IMAGE', 'https://cdn.chotot.com/sSw-uSGklb92QFFrym09qOYq0CSXmQICY_9615X6I48/preset:view/plain/58a150d4f4aae8a0e24c7e6ca155568d-2974401837634042280.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8822808a-2649-46ec-bd95-3766d8821cef', '325a356f-fb87-4b1a-b270-b0069fa4c6a8', 'IMAGE', 'https://cdn.chotot.com/6pUnuOW715NfnrwUPmEIhdSz8DpAp36hPXJ7GWVClcg/preset:view/plain/43671362829794f219e32491370ff249-2974401837735295293.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3b298dcb-89b2-488d-bfc6-699d81d132d5', '325a356f-fb87-4b1a-b270-b0069fa4c6a8', 'IMAGE', 'https://cdn.chotot.com/hg3sOQ_v2Adir4xYY3B-3XoJ8cRSBgNDKhIk7hlqVkQ/preset:view/plain/bb04147de28f8faa87add6e1c39423d3-2974401837400625870.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('35d5f5ff-3c7d-43bb-80ba-84882e3d1e85', '325a356f-fb87-4b1a-b270-b0069fa4c6a8', 'IMAGE', 'https://cdn.chotot.com/vEMWIqOYzAMbbr9ao7wgeTTQkMEP9YIVzpnAGYzyAng/preset:view/plain/b8dbc57ed37014b1645525ba2521e7f5-2974401837447888747.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('007c651b-3696-4e47-886f-950f04a56413', '325a356f-fb87-4b1a-b270-b0069fa4c6a8', 'IMAGE', 'https://cdn.chotot.com/2t0_bHlTBTmkx3fY-MrS4jUPFc0eWm-tAoPwUphS_Nc/preset:view/plain/b04cd34605419fa260c6f1b35938e508-2974401837173650951.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4099b8c6-0ea3-4c5d-9474-c57380b39847', '325a356f-fb87-4b1a-b270-b0069fa4c6a8', 'IMAGE', 'https://cdn.chotot.com/U2QEVco9WuUayzf7YAXX9pA3Doz-0grhNF0ZDPOVcHI/preset:view/plain/14a39434af5b311c104f4a82083c77b2-2974401837835289216.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ddd2f8e7-1ba6-4c09-840f-9ed7530f45fb', '325a356f-fb87-4b1a-b270-b0069fa4c6a8', 'IMAGE', 'https://cdn.chotot.com/LsXhyJkOYftplF4xFAMJlL3vqAHa5opswn3iKGZQCBE/preset:view/plain/9813e7db67aa8570a3e575eab210f12f-2974401838556591884.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('4359aebe-d318-416b-a325-5c0aa3a45161', 'P_132997838', 'APARTMENT', 'Bán chung cư An Sương lô A4, đã có sổ hồng riêng, chính chủ đăng bán.', 'Chính chủ cần bán phòng 404 Lô A4 chung cư An Sương, đã có sổ hồng riêng, nhà đẹp chung cư mới sơn lại. ', 'UNDER_OFFER', 'Quận 12, Tp Hồ Chí Minh', 54.5998, 1900000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4e4a1a14-4ebd-4b40-b576-6eb5e28e3106', '4359aebe-d318-416b-a325-5c0aa3a45161', 'IMAGE', 'https://cdn.chotot.com/NWkrggscLQIJJB9xp_U9soTX77RpM4N7Uj3tTBUAKwI/preset:view/plain/52362b3a09895a09ab88b82af37ffba7-2988914591788773200.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dd2d97ef-cbad-49fe-a056-dbbc36c47b5f', '4359aebe-d318-416b-a325-5c0aa3a45161', 'IMAGE', 'https://cdn.chotot.com/ge5BAXWpiFY8mv_gNydYx1jPBW6J_IObIkb9U9TI-A8/preset:view/plain/54c93cf3c8e131ff93ea0a30eaee7822-2988914591903558028.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1761d3c9-3538-4561-925f-33172266d242', '4359aebe-d318-416b-a325-5c0aa3a45161', 'IMAGE', 'https://cdn.chotot.com/u69yyiXzwqd6VFn_VMS7juZ-2aoXeCKykZlL9ZY69w4/preset:view/plain/0cf747d402ff485cc0fd11b0137cb3c7-2988914591955961939.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e0e17298-aef0-41d8-8811-eac84380871a', '4359aebe-d318-416b-a325-5c0aa3a45161', 'IMAGE', 'https://cdn.chotot.com/XlDbH4sSYCc9LjpQGKUtd_5SCSMDOHuiZRcHDVUJleg/preset:view/plain/1c35db358ea545afc48e4de3936bfccc-2988914591903622848.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('27d7085e-43b3-4e23-ae0b-9663ee217151', '4359aebe-d318-416b-a325-5c0aa3a45161', 'IMAGE', 'https://cdn.chotot.com/ErriRsLjNt8GfyNu8r8FRRO2DQ6Eftjrf0Va3PJ8wxs/preset:view/plain/9494d2cacd549c0f4f69c202b46fd3e5-2988914592011714660.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a423cf44-2240-435c-8c84-ec9789d95650', '4359aebe-d318-416b-a325-5c0aa3a45161', 'IMAGE', 'https://cdn.chotot.com/bHCJZdzHFD1SByhmnBktCbpSO8G0BJScSv7nToLl0dE/preset:view/plain/092e188a5058bcd70646e86b14359fc2-2988914592011614107.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5f3d5552-8934-4648-b438-754b0c611427', '4359aebe-d318-416b-a325-5c0aa3a45161', 'IMAGE', 'https://cdn.chotot.com/mXYXPYYlyolvQ6q910QbxdG8j9DOZ4MyOV-BfQvxYXQ/preset:view/plain/f2d7afabe01015bb5546bd8513e339cb-2988914592329157633.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ee689488-df4e-4a74-ba36-2bd6b5b8e902', '4359aebe-d318-416b-a325-5c0aa3a45161', 'IMAGE', 'https://cdn.chotot.com/ayoIevnYusiEWBF7E87A3i3GQCD1EAZp8ky5Q8YEdq0/preset:view/plain/192ebb87c374ae07fb3866ad3b73c4f4-2988914592807956493.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3a807664-69e5-4533-a5d6-25b0975b0abd', '4359aebe-d318-416b-a325-5c0aa3a45161', 'IMAGE', 'https://cdn.chotot.com/OMfk5qmmb-2o95kl2VV_qhgv27ry3DP6MyAq1dVclFs/preset:view/plain/0ae478c14751d46c1d1968989ca5afd4-2988914592886962207.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('69f10c93-b784-489f-864f-f262bf0a74f5', 'P_133940886', 'APARTMENT', '💃 CHO THUÊ CĂN HỘ 2PN RỘNG 70M2 Ở TRẦN QUANG KHẢI QUẬN 1', '💃 CHO THUÊ CĂN HỘ 2PN RỘNG 70M2 Ở TRẦN QUANG KHẢI QUẬN 1
✨✨✨✨
✅ Căn hộ cao cấp, có đầy đủ tiện ích 
✅ Có hầm xe, thang máy, bảo vệ, lễ tân
✅ Vị trí căn hộ nằm ở trung tâm quận 3.  Thuận tiện di chuyển tới các quận khác chỉ 5 phút
✅ Có hỗ trợ khách nước ngoài, khách Việt,...
✅ Có hỗ trợ xuất VAT nếu khách có nhu cầu
_____
Liên hệ *** (Lê Duyên - hỗ trợ tìm phòng 24/7)
', 'AVAILABLE', 'Quận 1, Tp Hồ Chí Minh', 70, 14000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1da4ecaf-73b4-4c03-991c-a12bdd698f40', '69f10c93-b784-489f-864f-f262bf0a74f5', 'IMAGE', 'https://cdn.chotot.com/AuZDtAZy_m8n738LjrQF12zJX2qQbpwkHYFgQMrISi4/preset:view/plain/55f58dc27d8baa09e58076337fdd4b7a-2996122482029732900.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3c7dffdc-9e06-47a9-90d5-a90f5c3c8265', '69f10c93-b784-489f-864f-f262bf0a74f5', 'IMAGE', 'https://cdn.chotot.com/6Q2zq6eX-T2Sr1hYYmRk66tMxm4hZp3KiwqlUV0VwzI/preset:view/plain/d452a64c9473a23e512fc41a4db7d971-2996122481961125348.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f658c089-10b2-46f1-91f6-3bfb7a2b8c70', '69f10c93-b784-489f-864f-f262bf0a74f5', 'IMAGE', 'https://cdn.chotot.com/a3SrvL1oGy9qHspIh340JoHXzd90XEOjLuW3JaAQfk8/preset:view/plain/def5e6be305a95309b969cc93678c0a3-2996122483472639012.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('87a7db20-5492-43ab-97c9-997d7783ec0d', '69f10c93-b784-489f-864f-f262bf0a74f5', 'IMAGE', 'https://cdn.chotot.com/eC9ID880_1keW8vkjQFj46YtM2aT-YjCgpPCgf1cSgs/preset:view/plain/8f70de451275665220af8af4feab07da-2996122483471140324.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9dd3bd7a-aa38-4c89-b1ac-43644aec9cd5', '69f10c93-b784-489f-864f-f262bf0a74f5', 'IMAGE', 'https://cdn.chotot.com/XFAdd-5_yoqnzjWQ34kxGZcXxplZBvnIislH0CVjFJY/preset:view/plain/d748a91a3f4ed78f14e4dda5c00eb5a0-2996122484735691129.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6a7b1a43-e85d-405b-a809-972be39a92bb', '69f10c93-b784-489f-864f-f262bf0a74f5', 'IMAGE', 'https://cdn.chotot.com/C4CgOVypz6inDs2vmnAiREixAoJIhc3ze6IxzXtGKic/preset:view/plain/d1f575009c4ae0ff4a73e22a0656eafd-2996122484846937572.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ae4fc75b-89f8-4a73-b851-e3d3270eddaa', '69f10c93-b784-489f-864f-f262bf0a74f5', 'IMAGE', 'https://cdn.chotot.com/uHM3yb2zQUkoHYtxqmTK_5dmt-6sH7IriKXsk07-88Y/preset:view/plain/278068b769d67b3bc56cd970f14fd9f6-2996122486010825081.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2813cf4b-a7f2-4fce-a2a0-eb6ad8399c5f', '69f10c93-b784-489f-864f-f262bf0a74f5', 'IMAGE', 'https://cdn.chotot.com/XNLh3BVpWsq4vqwZ8GEz_0gkzvDs0e4DP-gEV26_lcI/preset:view/plain/9a6a3ad349c950972f95ffe81880320c-2996122486138848740.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3bda5815-1ffd-4f2f-903a-cb611a0d00fd', '69f10c93-b784-489f-864f-f262bf0a74f5', 'IMAGE', 'https://cdn.chotot.com/YcSpkZlYLJV-CaDAx5FcsUA2rgXf_EVdT2WrJHKSPDs/preset:view/plain/4b8f1745a5c56a3b8ee54e4f40a8024f-2996122487262987748.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('997f4e29-165b-4c56-8b6a-8f4101d3b51b', '69f10c93-b784-489f-864f-f262bf0a74f5', 'IMAGE', 'https://cdn.chotot.com/QzTicFsek4kxWYQlfVx3KFM6blaxqi5reDtBzZQCqvE/preset:view/plain/1f682eded4e02396679861a4812f03cc-2996122487420176761.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('951e5bca-ab5c-4322-b1bc-b96ae0dd0dc2', '69f10c93-b784-489f-864f-f262bf0a74f5', 'IMAGE', 'https://cdn.chotot.com/oCoY0nquvMJjkT5kxY-zPy1kM7NgSPrioU5k9ztfFSo/preset:view/plain/66501fa855fa25eba2cf1e9741a7a6a5-2996122488689116644.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('4de205f1-97c9-4a99-9038-b5959e14bf45', 'P_133940887', 'APARTMENT', 'Cho thuê căn hộ Akari City 2 Phòng Ngủ 1 Nhà Vệ Sinh 61m2', 'Dự án: 
Thông tin chi tiết: Cho thuê căn hộ Akari City 
2 Phòng Ngủ 1 Nhà Vệ Sinh 
diện tích 61m2 
Giai đoạn 2 còn được miễn phí quản lý 
nhà có ban công 
nhà nội thất cơ bản có rèm giàn phơi
-Akari City nằm tại 77 đại lộ Võ Văn Kiệt, phường An Lạc, quận Bình Tân, TP.HCM -Dự án có nhiều tiện ích nội khu như hồ bơi, gym, siêu thị, nhà hàng, café, khu vui chơi trẻ em, mảng xanh và không gian sinh hoạt cộng đồng.  -Phí quản lý: 13.500 đồng/m² với Giai đoạn 1 , Giai đoạn 2 đang miễn phí -Phí gửi xe có bảng riêng theo từng loại xe và thời điểm.  -Điện nước cư dân thanh toán theo thực tế sử dụng.', 'SOLD', 'Quận Bình Tân, Tp Hồ Chí Minh', 61, 8500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('da0c7511-d077-41c5-8041-1fab241ff3cf', '4de205f1-97c9-4a99-9038-b5959e14bf45', 'IMAGE', 'https://cdn.chotot.com/3SoWuk2BAa7uQ_TK1H9pIA_FVblOtgYYLgbq856bXK4/preset:view/plain/59bd3aa9637661a7b3b96e0472a104f9-2996122967519643108.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e1f654ec-499e-4a44-b677-39a8f4b47d04', '4de205f1-97c9-4a99-9038-b5959e14bf45', 'IMAGE', 'https://cdn.chotot.com/0HLtd43dJQzGnFagU2gCnrX59Qtc6E6jyJtZms-SJus/preset:view/plain/e4bf4e97a7ce5aaee255913776b2e035-2996122967842246247.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('29faced0-54f4-4469-b1e6-797078d4c76f', '4de205f1-97c9-4a99-9038-b5959e14bf45', 'IMAGE', 'https://cdn.chotot.com/eSRzvEEHTOJkXGXPy1Oc6Yg_s2vMl3h8j67QMSBpnLI/preset:view/plain/12c674cf2696f00a9850d757772994f6-2996122968069547044.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('68f1d18a-5c97-4de4-b439-f90eaa83cf22', '4de205f1-97c9-4a99-9038-b5959e14bf45', 'IMAGE', 'https://cdn.chotot.com/pxzKgN5osyuX79JNv4bdTZCMeHr9jdHNV08U9WhA9HE/preset:view/plain/e60fe42bd00745312dc93841723d68bb-2996122968033809415.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dda58302-251a-47b4-bfb9-fb927c19c4d8', '4de205f1-97c9-4a99-9038-b5959e14bf45', 'IMAGE', 'https://cdn.chotot.com/73zYKvOK8ZlCG7M6xiLDpDsyHGN8F7bnaBUg0iuSLdQ/preset:view/plain/56973e999b23b13658ebe8e3ed61e9cc-2996122968100529305.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4fdb74f5-0efd-4bca-9d81-cb17a40c9ad4', '4de205f1-97c9-4a99-9038-b5959e14bf45', 'IMAGE', 'https://cdn.chotot.com/_jJK4uLgy7BcHp7lvgpoEINIOWCx9Vn09O9zcqBnsyg/preset:view/plain/e06d36405914beb7bde7ab6be738a80e-2996122967858271231.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b2c290f3-1324-4071-b4bd-f88b73b646f8', '4de205f1-97c9-4a99-9038-b5959e14bf45', 'IMAGE', 'https://cdn.chotot.com/pClvfiEcSTgeTh3aTKnP1j8WprWcRZQsFpNcRjDxAu0/preset:view/plain/ada0bd5942f89eb428c820b2527a543c-2996122967907342489.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c3052911-ab83-411b-b532-9bc878c1e487', '4de205f1-97c9-4a99-9038-b5959e14bf45', 'IMAGE', 'https://cdn.chotot.com/tm7q2stcNeoBp1v6zdf8JQFUmgiIaR0haWOxjsgJIRE/preset:view/plain/14cb54f1264c03907a737490cefe53bd-2996122967912302969.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('220bb2ed-25ea-4ed0-a2b6-484752cb1a7b', 'P_133940882', 'APARTMENT', 'Căn hộ Studio 35m2, 100% Q7 - Gần Lotte,Kcx, Đh Tdtu, Rmit', 'Dự án: 
Thông tin chi tiết: Căn hộ studio siêu thoáng 35m2, 100% Q7 - Gần Lotte,Kcx, Đh Tdtu, Rmit 

Địa chỉ: 142 nguyễn thị thập, quận 7 

Gần Lotte Mart, Crescent Mall, KCX Tân Thuận, RMIT, TDTU. Thuận tiện đi Quận 1, Quận 4.

Full nội thất, máy giặt riêng, phòng rộng thoáng, dọn vào ở ngay.

Không chung chủ, giờ giấc tự do.

Liên hệ xem phòng', 'UNDER_OFFER', 'Quận 7, Tp Hồ Chí Minh', 35, 6300000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('752a084d-25ec-4e5c-9f05-2ff9da4fe1ff', '220bb2ed-25ea-4ed0-a2b6-484752cb1a7b', 'IMAGE', 'https://cdn.chotot.com/Za-5o_-eX6QebNrc4dRDLi8bs2LewIgpVartkseWVDA/preset:view/plain/0e8d011cb80d0ac60f905b424c5bc0fb-2996122872762505369.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('11362bb4-15c1-420e-b394-30e3e1f1ec10', '220bb2ed-25ea-4ed0-a2b6-484752cb1a7b', 'IMAGE', 'https://cdn.chotot.com/b_QYj9prIw6LJPrFzcpl2rCR13DyFt5afk_KMlLcAjw/preset:view/plain/09f6d001d2a70fa4cd3759fc8b29dfbb-2996122872965713511.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6278e2f5-165e-4034-a1f2-5a7f6ee1923b', '220bb2ed-25ea-4ed0-a2b6-484752cb1a7b', 'IMAGE', 'https://cdn.chotot.com/owr9DOn9nH1-1SJruqNdL6yZ30SJZH8NZAOP5TGZlEk/preset:view/plain/9655fe5d4187d6474f4fcf2ee9288799-2996122873209752629.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2874b6bf-3b35-4e54-96c4-7a5e3e56a7b5', '220bb2ed-25ea-4ed0-a2b6-484752cb1a7b', 'IMAGE', 'https://cdn.chotot.com/Hu8ooPR539uBi0rrlUBV9TP-H2F8Y5atlton_kQ5rwg/preset:view/plain/319d78b575a7393c3bbc85f577a4e12f-2996122872980727462.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0bfe5420-f00b-4776-89ef-ce12f86a4c99', '220bb2ed-25ea-4ed0-a2b6-484752cb1a7b', 'IMAGE', 'https://cdn.chotot.com/QSRpYVs8-nTnjh0ZLzw0RQAvkCRW1p17SneYG3EqsQ0/preset:view/plain/2cdb7c706965445b3e897e916391f731-2996122873038577752.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ff4ba59e-782c-44b1-bac3-f49b464f8e68', '220bb2ed-25ea-4ed0-a2b6-484752cb1a7b', 'IMAGE', 'https://cdn.chotot.com/wJ51EgLUO62xSrBRYwDCPwcIXInmfGUjgm3N6igkGds/preset:view/plain/19f5bd537c704513250c60a1e07a025c-2996122873208656903.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8f4993a5-ec9f-4570-9314-c85a11654e24', '220bb2ed-25ea-4ed0-a2b6-484752cb1a7b', 'IMAGE', 'https://cdn.chotot.com/h9MzCvijiQZG5IyEX069Q_dWol3tt1K4le_SIPTVbJY/preset:view/plain/b337d275ccffa85fa21e80fc1d8f09fe-2996122873267606527.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('548925b6-63bd-4b55-a0b3-626fd3eb5003', '220bb2ed-25ea-4ed0-a2b6-484752cb1a7b', 'IMAGE', 'https://cdn.chotot.com/NZp0n36yV6Hx1FcUI1tV7dRjFDucdoHHWbJTzWsRVMU/preset:view/plain/14e547b899de693a40baf3931747186a-2996122873258665113.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('134c382c-1709-463d-a929-6636497bc4ec', 'P_131723167', 'APARTMENT', 'Bán chung cư Westgate 59m2 - giá 2,68 tỷ - 2pn2wc - sổ hồng sẵn', 'Chung cư WestGate - Trung Tâm Hành Chính
Căn hộ 59m2 ( 2pn2wc )
+ Giá 2.680.000.000 đồng, bao thuế phí
+ Sổ hồng sẵn
+ Hỗ trợ vay ngân hàng tối đa
+ Nội thất : full bếp
- Rèm và giàn phơi
- Nhà đang trống, dễ thiết kế nội thất theo ý
Liên hệ : ***', 'SOLD', 'Huyện Bình Chánh, Tp Hồ Chí Minh', 59, 2680000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('74175865-432f-4666-83ea-fa93fe08d13e', '134c382c-1709-463d-a929-6636497bc4ec', 'IMAGE', 'https://cdn.chotot.com/PWNBbJWcTYyzjv-wKZrxwsA0psyeJl1wKSQkc3aSSJY/preset:view/plain/f4e790834a78c94e3932dfc827411e0b-2986601106274084446.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('513724bd-4c3a-48e7-8d65-e3db93fe9cbd', '134c382c-1709-463d-a929-6636497bc4ec', 'IMAGE', 'https://cdn.chotot.com/DcCaV_jBrHrwimwuLX7mU8l_-z-S5soWTYaKPBXhlsA/preset:view/plain/78d515d13143657082fa009504ccbd0c-2986601301080922212.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1aaa0c91-5871-4af6-ba4c-354e9e6bb0fc', '134c382c-1709-463d-a929-6636497bc4ec', 'IMAGE', 'https://cdn.chotot.com/PMcMMRKixKSk-vUIgCn3K2ixQ0z4P0O76kLZjQZdkMg/preset:view/plain/ba0fc51e85c743a903625fc0f9fc3d8f-2986601304634900945.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('59ffabac-f554-4856-a12e-7887a867c0b7', '134c382c-1709-463d-a929-6636497bc4ec', 'IMAGE', 'https://cdn.chotot.com/0jBsjhJZF0JV0e0zF3tJVjFxi1QaPTz9v66nMZdLqdk/preset:view/plain/ffa6cad1589ba6ab069e8b6a62e1ee88-2986601304567801438.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('74274cd7-6419-4c3e-a7bc-6323ebfb767d', '134c382c-1709-463d-a929-6636497bc4ec', 'IMAGE', 'https://cdn.chotot.com/jyi0cU551pfiOWEwJyHhNqjpEqLAQPsebQh-Gw9fk4M/preset:view/plain/12ae22e4f7fbda58e4634c258ed283ac-2986601303880779801.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a9d939dc-0430-447a-87d7-90fffed3bdc8', '134c382c-1709-463d-a929-6636497bc4ec', 'IMAGE', 'https://cdn.chotot.com/EqTMS_dwqPQL8vwu4zzJ-Yho-5-cTQ03_yoa4M8OOcA/preset:view/plain/f9881f02179c63adfc0c56f5037bd358-2986601301933703633.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('daac8ce7-4f97-45ec-9a96-5732823f9490', '134c382c-1709-463d-a929-6636497bc4ec', 'IMAGE', 'https://cdn.chotot.com/yymxRj_MF9IFnvTYysZO6MFFAK6md6nYksakJf3aGxs/preset:view/plain/d86f270db1a2523e7953b74fcb9d5506-2986601302067930718.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('ab314766-0dbe-406a-8415-70266193f5a6', 'P_133940879', 'APARTMENT', 'Căn hộ M-One 2PN 1WC 65m2 full nội thất', 'Cho thuê căn hộ chung cư M-One Nam Sài Gòn
- Thiết kế: 2 phòng ngủ 1 WC, có ban công
- Diện tích: 65m2
- Tầng cao, view thoáng mát
- Trang bị đầy đủ nội thất, chỉ xách vali vào ở
- Tiện ích chung cư: hồ bơi, phòng tập gym, bbq, khu vui chơi trẻ em, cafe, siêu thị,...
- Giá thuê chỉ 13 triệu/tháng', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 65, 13000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f3599276-9743-462c-94d9-4f36af7a300f', 'ab314766-0dbe-406a-8415-70266193f5a6', 'IMAGE', 'https://cdn.chotot.com/9fY-uXpulh2jl7vDYSONE8VP0c5_nxgs9Y4zi9W6lig/preset:property_project_small/plain/158_overview_1.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fc44f94f-4ab9-4b4b-b638-e866367ceee2', 'ab314766-0dbe-406a-8415-70266193f5a6', 'IMAGE', 'https://cdn.chotot.com/t3Cab-fKY8iQlkL9njeL6z4yMnE9frdyLOFuENkAchc/preset:property_project_small/plain/158_facilities_4.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('529817b6-6a94-4f91-a1c3-8cdff86125b6', 'ab314766-0dbe-406a-8415-70266193f5a6', 'IMAGE', 'https://cdn.chotot.com/jYMvGKjCwLYu_GHHYteqdkXdM4-v63a9RKlztdJZkDE/preset:property_project_small/plain/158_sample_house_5.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('30f62662-6ab4-4caf-81e6-dcb5e6a963fb', 'P_132191827', 'APARTMENT', 'Phòng Gác Full Nội Thất Giá sinh viên Quận 7', 'Dự án: 
Thông tin chi tiết: DUPLEX  SIÊU RỘNG FULL NỘI THẤT NEW 100%

Đầy đủ nội thất như hình: tủ quần áo, nệm, tủ lạnh,…
Phòng rộng thoáng mát phù hợp ở 4 người
Có ban công đón gió lấy sáng
Thuận tiện qua Q4, Q1, Q8
Có khu giặt phơi chung', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 35, 4400000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c6dccb07-0165-4fab-a548-9f9505fbb5e5', '30f62662-6ab4-4caf-81e6-dcb5e6a963fb', 'IMAGE', 'https://cdn.chotot.com/aJzYqA4ckn_u2dYEyqXBboMy7FxB9YBDoVwoCire3MQ/preset:view/plain/ee50cdb7895f7ae80f7361beb1553528-2982903821745177642.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cb1a7768-ed06-41e1-9292-3342e3918a3e', '30f62662-6ab4-4caf-81e6-dcb5e6a963fb', 'IMAGE', 'https://cdn.chotot.com/Dmiv2ogJ0E66kRpA9EJxDb8J1v3s2v2JpyR0EaYwEJc/preset:view/plain/7e86064db892dbdae0db22879bfe2cca-2982903821784873348.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ced5376d-e5a3-4330-a94e-53b95de7fb7b', '30f62662-6ab4-4caf-81e6-dcb5e6a963fb', 'IMAGE', 'https://cdn.chotot.com/zk34kCtMV79aSeC5dpa10HjnYqwlYf1GUe7AdeM5N2c/preset:view/plain/99534d014f2ec8556f189695932c9928-2982903821855570781.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5644c664-5987-42ba-b596-31741264582a', '30f62662-6ab4-4caf-81e6-dcb5e6a963fb', 'IMAGE', 'https://cdn.chotot.com/_j0PkOWOwspFtypknCfelJY9Q9_E19NAeQK7W77W1pc/preset:view/plain/5755787e910be9e83f5bbb6d70808644-2982903821983696807.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('39a1a1ff-7545-4b89-942d-6b79fb73c865', 'P_133940870', 'APARTMENT', 'Cho thuê Cc WestGate - giá 6,5 triệu - 2pn - sẵn 1 máy lạnh', 'Dự án: 
Thông tin chi tiết: Chung cư WestGate - 59m2 ( 2pn2wc ) 
- Giá thuê : 6,5 triệu / tháng
- Cọc 2 tháng
- Hỗ trợ đăng ký tạm trú
- Nội thất :
+ Giường, tủ quần áo, tủ giày
+ Máy lạnh
+ Rèm và giàn phơi
Liên hệ : ***', 'AVAILABLE', 'Huyện Bình Chánh, Tp Hồ Chí Minh', 59, 6500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f53d9340-c83f-46ac-bbb5-315d8de39865', '39a1a1ff-7545-4b89-942d-6b79fb73c865', 'IMAGE', 'https://cdn.chotot.com/soYtx9Fo6aLdTc1F4_hE8N5sIrgzSnu9CUdNgd9qaHU/preset:view/plain/5389a40abf98fb486443b950f50d0aee-2996122629452973540.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2b286b6a-bc36-4458-96dd-45971d187980', '39a1a1ff-7545-4b89-942d-6b79fb73c865', 'IMAGE', 'https://cdn.chotot.com/AmXi0WxhRN1MGtXIpK-F-loisPgr7GDAAK14_842m28/preset:view/plain/3e6ea80cecf1285cb642698d95c54339-2996122629492132217.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0e2455c5-eced-4574-b4a6-f46f0cd85118', '39a1a1ff-7545-4b89-942d-6b79fb73c865', 'IMAGE', 'https://cdn.chotot.com/LyTzENLmNY2k728csynJL49Hs6OsZCEDzrcUFG0AguU/preset:view/plain/827b1a3bf3db64aef0ab0f44fa1bd425-2996122629540124825.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f9dc57ff-04bb-4431-ba1d-64f16fab07a8', '39a1a1ff-7545-4b89-942d-6b79fb73c865', 'IMAGE', 'https://cdn.chotot.com/EZmVGuopuBjw5E5pTpoDxBlZFrtm6k6Tem750-LoWow/preset:view/plain/e12c5e71e7ed81fb072a566a9b5c6fa5-2996122629610525695.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0d1451c4-729b-48e5-b435-c3114d1ed240', '39a1a1ff-7545-4b89-942d-6b79fb73c865', 'IMAGE', 'https://cdn.chotot.com/DtBBsF6IZihs58eecfbAwLLadqJk-d7QNIH6AXmjfKU/preset:view/plain/2e4846a7938dce13bef81c36ab7fd1de-2996122629637514276.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6e2dfe6d-e44f-4635-9b29-40399ff06cb0', '39a1a1ff-7545-4b89-942d-6b79fb73c865', 'IMAGE', 'https://cdn.chotot.com/j4IeCeA2RN6GOIsqvSA2lro3QbSr8IQwi1hYo2fq8Os/preset:view/plain/8f7299e417923b27959f67d0e1f38c87-2996122629781035089.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0c5ee273-b534-4a8d-92d2-4a7ad58acfae', '39a1a1ff-7545-4b89-942d-6b79fb73c865', 'IMAGE', 'https://cdn.chotot.com/tMZxtzzBYEI2iedptvkRwn_bU18fjBm-EHUOPnSyMBQ/preset:view/plain/2fe432fd701a96f0396a32ec04e8f95f-2996122629736053485.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('38ef27ef-c094-48e9-a1c3-6379e985f636', '39a1a1ff-7545-4b89-942d-6b79fb73c865', 'IMAGE', 'https://cdn.chotot.com/SaUwtbwCyci7P_OptQsjCAxjhtoGGpGPKmJiJzMYkFQ/preset:view/plain/8ebb5e57a9a5fdd30d240495a002db0f-2996122629744060070.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0d406d6a-35ca-403f-89eb-374a9033ab5d', '39a1a1ff-7545-4b89-942d-6b79fb73c865', 'IMAGE', 'https://cdn.chotot.com/uAvLe5aYffn6OgdXLVlnMKDdgxP7p4Ll_F-fvhAVgBw/preset:view/plain/a3ce7ae0b08674c7a387c09d81a2be9d-2996122630464556647.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('74bbaca4-530f-4b8b-a1de-bd892dde42af', '39a1a1ff-7545-4b89-942d-6b79fb73c865', 'IMAGE', 'https://cdn.chotot.com/ZDyC7jl3kNJ_MuW7xCgnjmEARQe7KdUEK53DtNpqLJk/preset:view/plain/90eb03c284ec4206fd45932e500929e8-2996122629801320536.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('32cb0a48-020b-43d7-ace2-03185c012c5f', 'P_133940864', 'APARTMENT', 'Cho thuê căn 2 PN, Cách Mạng Tháng Tám, có ban công có cửa sổ', '2PN - xxx/xxx Cách Mạng Tháng Tám, Phường 4, Quận 3 (Phường Xuân Hòa), TS 59m²
✨ Có ban công
✨ Có cửa sổ
----------------
_PHỤ PHÍ:
- Điện: 3.500
- Nước: 150.000
- Gửi xe: Miễn phí 2 xe
- Dịch vụ: 200.000

', 'UNDER_OFFER', 'Quận 3, Tp Hồ Chí Minh', 59, 17000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('707b4830-9413-4914-8da5-82aa7b5caf96', '32cb0a48-020b-43d7-ace2-03185c012c5f', 'IMAGE', 'https://cdn.chotot.com/uHLbbWR3T_S_S_bj9diYT7dX4JJ110bPV5O5BuVjaiY/preset:view/plain/da2aac7cba67c4a937bfe2bd11c53238-2996122784607982599.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('381d2dc7-62c0-4e22-881b-4b7af3cb7185', '32cb0a48-020b-43d7-ace2-03185c012c5f', 'IMAGE', 'https://cdn.chotot.com/m3IOOqo_X5cm3J3hYbIqfQ5LY1g5YGPVybPMS8e_r-4/preset:view/plain/bbe028a52196a12298b384514b0f8a6f-2996122784263327335.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('acb9f3a9-9b96-4d57-a24b-a8e75bfd73c1', '32cb0a48-020b-43d7-ace2-03185c012c5f', 'IMAGE', 'https://cdn.chotot.com/WRjz53xErprPo-HDU6T9DbYsv46JwxXeoQ4ABdjtJlw/preset:view/plain/2db8978405ed1ab06786cebc0d0b1856-2996122784514336422.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('80d8fecb-8f0c-4082-8dd0-c87eaa025dd2', '32cb0a48-020b-43d7-ace2-03185c012c5f', 'IMAGE', 'https://cdn.chotot.com/xvSITlTvOPDGZpDm8mS0LSbsAqsneexBLgo2JPsqQW4/preset:view/plain/3b5d16fa7d4dbc5589541e494a77ec3b-2996122811778485863.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0ece143a-431b-45c6-aba2-48df89e45a25', '32cb0a48-020b-43d7-ace2-03185c012c5f', 'IMAGE', 'https://cdn.chotot.com/Y01O9f_rqXkQ3u2xP4RnIt6R_ma_TViSF5ap8ueFc20/preset:view/plain/bdb8e84768f7adf4f5cb3b25e413a7ce-2996122811998115112.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0b8962b8-6db6-4be1-9ba0-36d47a86043a', '32cb0a48-020b-43d7-ace2-03185c012c5f', 'IMAGE', 'https://cdn.chotot.com/AGFyaaIKr9vSF24dzxlo1GMrZRQwB1M_dgtK71t3kUs/preset:view/plain/68f5ece4ac427b5ece4fba22202444fb-2996122812131038207.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('74045199-6de1-4c12-87c9-8eca80d9f53c', '32cb0a48-020b-43d7-ace2-03185c012c5f', 'IMAGE', 'https://cdn.chotot.com/haBRgVkyJnGWlUQYwXr3UbzL4UssY74sYYX7sZs0Pq8/preset:view/plain/5fd2932d34eaaf3460c5e2cc192c8725-2996122812247014925.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('bc6d3b2e-7db7-416b-b91b-45f436e8ec37', 'P_133708454', 'APARTMENT', '2 PHÒNG NGỦ FELIZ EN VISTA FULL NT ĐANG TRỐNG SẴN GIÁ CHỈ 25TR/ THÁNG', '2PN DUPLEX FELIZ EN VISTA CHO THUÊ- SẮP TRỐNG
🌿 Tầng thấp, view hồ bơi
🎄 Căn hộ full nội thất 
🍄 Giá chỉ: 25.000.000/ tháng 
Gọi ngay em ngay: *** Ms Thủy (call/zalo/viber) tư vấn và xem nhà 24/7
-----------------------------------
2BRs DUPLEX FELIZ EN VISTA FOR RENT – AVAILABLE SOON
🎀 Low floor, pool view 
♻️ Full Furniture
🌂Only price: 25 mil / month 
Tel: *** Ms Thuy (call/zalo/viber) support right now. 
', 'SOLD', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 102, 25000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('60115b29-575c-41ef-82fa-c53636b9984c', 'bc6d3b2e-7db7-416b-b91b-45f436e8ec37', 'IMAGE', 'https://cdn.chotot.com/pgZKyrTeb75XshKMNBKavcBTr93TbYoyCDiUOFPIWYY/preset:view/plain/362d0da4af214488a28568a385418633-2994359886441160853.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8f08966a-5f9d-43dc-9269-f2975b3cbc03', 'bc6d3b2e-7db7-416b-b91b-45f436e8ec37', 'IMAGE', 'https://cdn.chotot.com/zeewkydNh_XIYKRV5diveTNmu1ewWjbLYT0HO3cl7xY/preset:view/plain/3c90a6709ef381c0042775bea9e4d9c1-2994359887320047777.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ac2e492f-221d-4012-8e7a-e7620c007a62', 'bc6d3b2e-7db7-416b-b91b-45f436e8ec37', 'IMAGE', 'https://cdn.chotot.com/ira8MuRu4mNth36iFr-9BPbEisudGHaRJbmha61nRR0/preset:view/plain/3ce628ef4c27229d9b19d373203fb782-2994359887474661292.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c057caac-c517-4be3-8131-8cac614dd675', 'bc6d3b2e-7db7-416b-b91b-45f436e8ec37', 'IMAGE', 'https://cdn.chotot.com/nI70Ku_Y6dkhpnWNTt1eW-sQ7le3TuqED7pnm_jDQzU/preset:view/plain/40bf0eff28704a30e5e0573155e9a581-2994359887581594016.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1a2c7b7b-8adb-46d9-b259-be9eb2c0573c', 'bc6d3b2e-7db7-416b-b91b-45f436e8ec37', 'IMAGE', 'https://cdn.chotot.com/CnxYHJFNC60RsY_Xl0CtjAl41H8E4ZWkAQXexVkGric/preset:view/plain/9c45b2f0f02121ccd8e4d9afe0bf6f46-2994359887407206012.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c7f782e1-e4e1-4b73-a0b7-45371a92f959', 'bc6d3b2e-7db7-416b-b91b-45f436e8ec37', 'IMAGE', 'https://cdn.chotot.com/ts_8-cRVo7zO6XpQCNSrVDUsIuvyjShRFSjc00pblMk/preset:view/plain/573904c3539abdfa2aede07899a57248-2994359887426658897.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1198fb45-041a-4215-b7bc-268c848bce5e', 'bc6d3b2e-7db7-416b-b91b-45f436e8ec37', 'IMAGE', 'https://cdn.chotot.com/IbgoHNN1NZ9ZYT9LeHyfmqgoo-X61QRGYB0EBywnmbU/preset:view/plain/f4b306dd18fe6bbf23ef0f5bc150c603-2994359887749847957.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('eb36c6f7-ede5-4630-a93c-ecc1abd0c31e', 'bc6d3b2e-7db7-416b-b91b-45f436e8ec37', 'IMAGE', 'https://cdn.chotot.com/ZIeNZmT_1ebvKYOMbYqWY_7OYlvhkJYqZYtLICBrJyw/preset:view/plain/131e11ade8f78ef37da6cbd55e3b6565-2994359888069345711.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3d413a56-d5ad-464d-b799-24c0b8a72ac8', 'bc6d3b2e-7db7-416b-b91b-45f436e8ec37', 'IMAGE', 'https://cdn.chotot.com/DA2nS5SU0u8EmOMmimf0Co52D6HOVQMQ7oi12ZdjuFQ/preset:view/plain/899dff4356509b93dd9dd8064fe23e9b-2994359888561446764.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2262b9e1-8a8e-463d-866e-a12594a36e37', 'bc6d3b2e-7db7-416b-b91b-45f436e8ec37', 'IMAGE', 'https://cdn.chotot.com/tcPnUExChsIWPPFcMwmKDhgpJeN-3mr3KfDSVV9aWm8/preset:view/plain/352b25c8fcc0ea0721f75fa7a7088f55-2994359888085393557.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dd10f9ff-f8d8-4112-aac8-712cceba9fa0', 'bc6d3b2e-7db7-416b-b91b-45f436e8ec37', 'IMAGE', 'https://cdn.chotot.com/T8QQMmBBaFollKauJPMoPgvL26aTrVXhQXOTbj2RIzs/preset:view/plain/31a263050dc2771bd04ce953820d4eee-2994359888514797998.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('b77d979b-bf4d-465b-a2d3-512edcd2643c', 'P_133940859', 'APARTMENT', 'CHO THUÊ BAN CÔNG THOÁNG ĐỖ XUÂN HỢP, GLOBAL CITY, NGÃ TƯ BÌNH THÁI', 'Dự án: 
Thông tin chi tiết: 📍 659 Đỗ Xuân Hợp, Phước Long B Quận 9 

• Gần Ga Metro,Cầu Rạch Chiếc,Vincom Lê Văn Việt,Khu Công Nghệ Cao, Đỗ Xuân Hợp, Ngã Tư Bình Thái CĐ Kinh Tế Đối Ngoại, ĐH HUTECH, SPKT,.....

Tiện ích : 
+ Hệ thống pccc an toàn 
+ Ra vào cửa vân tây an ninh 
+ Giờ giấc tự do, không chung chủ
+ có thang máy 
+ Nội thất : máy lạnh, kệ bếp, tủ đồ,...
📞L.h / za.lo : *** ( Nhi Lưu ) để hỗ trợ xem phòng nhanh nhất,i.b để tư vấn', 'UNDER_OFFER', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 30, 4500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e761885c-22d3-4a52-9d0a-68e3366f6c47', 'b77d979b-bf4d-465b-a2d3-512edcd2643c', 'IMAGE', 'https://cdn.chotot.com/5fbm5iAsNuD2V9p17ztysilAPQrVbSppZvOOIyHzrFs/preset:view/plain/fba8eafa37324ab2f0c2c61791d90e7c-2996122514314382951.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('97087c59-fc5b-4096-a9ac-20b498d9ee5d', 'b77d979b-bf4d-465b-a2d3-512edcd2643c', 'IMAGE', 'https://cdn.chotot.com/8ZmAPLTASVEWjQYknPeK4Mg7soEn7vjnoB_ESt94xBg/preset:view/plain/14f6069334f4f976b53360461de53546-2996122514390196312.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('974b54d8-28d1-4a9f-b67e-d92ac66602a5', 'b77d979b-bf4d-465b-a2d3-512edcd2643c', 'IMAGE', 'https://cdn.chotot.com/jSN8by4W8LyfbqQqYeVOZbRO_SeGdbzZ2TSZDcipRSQ/preset:view/plain/69f4c3981f799db3e3df59e474ef2f57-2996122514392234733.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d7e10b77-b08a-4893-acdb-360b74090555', 'b77d979b-bf4d-465b-a2d3-512edcd2643c', 'IMAGE', 'https://cdn.chotot.com/EC2zw_E2rQfw0N_v31w9RkVAvO4XBex4aVFzckhMKuc/preset:view/plain/9bf5125432381fa2fe9ba205a7a52070-2996122514437150801.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('af282af9-f5e5-49b1-b42c-2e0e40a5ccbd', 'b77d979b-bf4d-465b-a2d3-512edcd2643c', 'IMAGE', 'https://cdn.chotot.com/osRELMR1tAtA8vVDQAS8TkRKAoCDy5nGfkD91iDQUnY/preset:view/plain/db76da7e2c35b3a70fb32458e9f562dc-2996122514434282495.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a6309c0c-9a1c-4a12-b7bd-b173d219c096', 'b77d979b-bf4d-465b-a2d3-512edcd2643c', 'IMAGE', 'https://cdn.chotot.com/AahFTzngI6Aynh2KnlRSGnCpTQJi5E1r-nHHbP9UgmM/preset:view/plain/655669ae7ebc941deb002a2e60e7c3b2-2996122514951982695.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('80ec547f-56eb-417b-bce7-a96353f11438', 'b77d979b-bf4d-465b-a2d3-512edcd2643c', 'IMAGE', 'https://cdn.chotot.com/IhJ0XuuAErpGZXFM8VIqf9VtmIUDBlZJ3fSV83lftAA/preset:view/plain/8c743010d614c2d699ea1b134c6e8cbf-2996122514378081159.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('865b5fb7-56d1-442a-a9df-37828c17602b', 'b77d979b-bf4d-465b-a2d3-512edcd2643c', 'IMAGE', 'https://cdn.chotot.com/m_N82AxbVfEfP3Ct1fBuRxM-VjDj8Itgpk3ZGQYBz9o/preset:view/plain/2ec61b19d38f512fc8e12eec9814d4c9-2996122514470573352.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3cfb8eae-924a-45fe-8e72-f3b6a12fdaec', 'b77d979b-bf4d-465b-a2d3-512edcd2643c', 'IMAGE', 'https://cdn.chotot.com/qJuLEiZrtVuPD-cawNGjWzediAod_afcWLi95AWLHk4/preset:view/plain/81fbf1b6de51186f1a5e0c29c505c30d-2996122514376729636.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('56920372-3108-4788-8ce5-d8ebe80bf338', 'P_132283230', 'APARTMENT', 'Cho Thuê Căn Hộ Dịch Vụ Quận 7 1PN gần LOTTE MART, CRESCENT MALL', 'Dự án: 
Thông tin chi tiết: Căn 1 phòng ngủ full nội thất với ban công trải dài cực hiếm, cửa sổ lớn đón gió và ánh sáng tự nhiên cả ngày. Không gian yên tĩnh, riêng tư, phù hợp ở lâu dài sau một ngày làm việc mệt mỏi.

Điểm mạnh của căn:
 • Ban công rộng thoáng kéo dài toàn phòng
 • View mở cực thoáng, không bí
 • Full nội thất mới, dọn vào ở ngay
 • Toà nhà mới, sạch sẽ, an ninh
 • Khu dân cư Sadeco yên tĩnh, dân trí cao

Vị trí thuận tiện:
 • Gần Lotte Mart, Phú Mỹ Hưng, Him Lam
 • Di chuyển nhanh qua Quận 1, Quận 4
 • Gần TDTU, RMIT, UFM
 • Xung quanh đầy đủ cafe, cửa hàng tiện lợi, quán ăn, gym

Contact Zalo/WhatsApp: *** (Ngọc - Reyna Ly)

Hỗ trợ tìm phòng theo nhu cầu từng khách hàng đến khi tìm được phòng ưng ý nhất.

#canhoquan7dep #chothuecanhoq/ #studioquan7 #canho1pnquan7 #fullntquan7 #canhogiarequan7 #canhomoique #canhodep #canhothangmay #canhobancong #phongtrodepquan7 #canhochinhchu #canhoanquan7 #canhotiennghi #canhoganquan1 #canhoq7viewdep #canhodichvuquan7 #canhohimlamdep #canhogandaytienich #canhoquan7fullnt #chothuecanhodichvu #troquan7 #thuephongtro #chothuenhatroganTDTU #chothuecanhominiganUFM #chothuecanhominiganTDTU #chothuenhatroganUFM #chothuecanhodichvuganLotteMart #chothuecanhodichvuganCauTanThuan #chothuenhatroganLotteMart #chothuecanhomini #chothuenhatrophongtro', 'SOLD', 'Huyện Nhà Bè, Tp Hồ Chí Minh', 45, 6500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('643ce272-b0f2-47d4-81a7-e4b38b708ec9', '56920372-3108-4788-8ce5-d8ebe80bf338', 'IMAGE', 'https://cdn.chotot.com/tPC_bDv4EaqNVfCFvkz8ZB6dzf8N2wHozYbc8MOzAdA/preset:view/plain/93470361e6f77d815f594463614bd61f-2983516897863369083.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8b132dab-9729-42a7-867c-23da7c5c46b2', '56920372-3108-4788-8ce5-d8ebe80bf338', 'IMAGE', 'https://cdn.chotot.com/W20xUDmQoVSbos9ReEFuRw0HOwvcC0LNtxcuhxmB6X8/preset:view/plain/877f8a527bbffc976e20057597f944d7-2983516896722693852.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b8a0fb3e-22c6-4968-b8a1-c004b96e5b75', '56920372-3108-4788-8ce5-d8ebe80bf338', 'IMAGE', 'https://cdn.chotot.com/x9g10hwrv3MVogXDT2F4JRQFu2DdZ4Y-9BLFZCzpdIg/preset:view/plain/a8aa4fc405d3a5fe5a2a081dfc4c8ce4-2983516896855299600.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('94628037-f1ab-46f4-82fa-91af0b7fc74e', '56920372-3108-4788-8ce5-d8ebe80bf338', 'IMAGE', 'https://cdn.chotot.com/ao1BQq7c1Lsebodpzfuwx4zSEXVzRwFn6FiwdbG80o4/preset:view/plain/c10c12f92f1c67c37f6a0e442d97fcfa-2983516896934930487.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('261096f6-e22b-4461-9f12-80476fc21469', '56920372-3108-4788-8ce5-d8ebe80bf338', 'IMAGE', 'https://cdn.chotot.com/1IYSHNCRvG1ntan5vdNIbmhyK9mSypO5ErebvqFyP5g/preset:view/plain/80aeb865e53823d6d5f9ed73671532a2-2983516897627117072.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dd58e149-1799-41a3-97d4-5ba0fceedda2', '56920372-3108-4788-8ce5-d8ebe80bf338', 'IMAGE', 'https://cdn.chotot.com/XF-qyrLvr_7S8TK4uap-trsj80xFH_0Z2tRiY_Q_8SU/preset:view/plain/16c223971e365d5fb68673f7673627da-2983516897675710811.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('218ef531-0509-43d9-b470-fd00d31d867f', '56920372-3108-4788-8ce5-d8ebe80bf338', 'IMAGE', 'https://cdn.chotot.com/KipSwLJJvFa3OOJM5MFkJZM97dNmXvisbzuiCuw1h-c/preset:view/plain/5f8202b6e6070957f6085ef76dff5cda-2983516897654770787.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('12e53900-49e2-4072-8ff2-260c6f61edeb', '56920372-3108-4788-8ce5-d8ebe80bf338', 'IMAGE', 'https://cdn.chotot.com/kKkJ2tlUf7kzaStvsQ9wkDZWsodYndAcJvW8l29WEds/preset:view/plain/8f5b89caa5042fe6e4440abce679d910-2983516897773624865.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('241d6645-0323-4dbf-8a46-44ebf54a77e3', '56920372-3108-4788-8ce5-d8ebe80bf338', 'IMAGE', 'https://cdn.chotot.com/_2tWH_6eEpCLGi48DxzUHlNg268tGS7Y2cy3JWA_Se8/preset:view/plain/bf5d5bedf936fbe14c7f7ded55ef4ffd-2983516897694077744.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('55f57485-6faf-4059-84c4-cb18afffcff3', 'P_130653280', 'APARTMENT', 'Studio Full nội thất tại quận 7 sát lotte mart', 'Studio Full nội thất quận 7 

• Với thiết kế độc đáo có cửa sổ siu thoáng view thiên nhiên

• Full nội thất cao cấp, đầy đủ tiện nghi 

• Hầm xe, thang máy, bảo vệ 24/24, giờ giấc tự do

• Phòng cam kết đẹp như hình 

• Tiện ích xung quanh gần: chợ, các cửa hàng tiện lợi, spa làm đẹp,Lotte Q7, phòng gym

• Thuận tiện di chuyển qua: KCX, CTT,…', 'SOLD', 'Quận 7, Tp Hồ Chí Minh', 25, 4400000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ea7f403f-ec63-490f-aa34-1b1356560210', '55f57485-6faf-4059-84c4-cb18afffcff3', 'IMAGE', 'https://cdn.chotot.com/KxYyyM4pVWzPd9pvWWpKCOazhYhGQmDYepjK97D-nq4/preset:view/plain/c68a3e68a9f5f7ab91dcbc66052d3151-2969862498687547854.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bb8cce18-fe75-46bd-b31e-48a38e1e8d45', '55f57485-6faf-4059-84c4-cb18afffcff3', 'IMAGE', 'https://cdn.chotot.com/1hpCdT7yXL54U9On01A9ptGq0AqnEN6_HOVKrEu2_AM/preset:view/plain/f01c78393a6b5f932515c88eaa7aadae-2969862498653783477.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c06fbfbe-e27f-45e8-8535-42705d134ffb', '55f57485-6faf-4059-84c4-cb18afffcff3', 'IMAGE', 'https://cdn.chotot.com/a5-hNP5oVf8NZx_Y6ImhrYYbwxozHYGTP1WvYRfOzkQ/preset:view/plain/11e703f38e63b48069a918f5865d86a5-2969862498653773423.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7297c278-5de4-4cc9-99dc-a9f2f7e93799', '55f57485-6faf-4059-84c4-cb18afffcff3', 'IMAGE', 'https://cdn.chotot.com/5ZoMj7f9EZa_ztBvmaqLh2DtxbnTjvFjSHEoUu8GdmU/preset:view/plain/5b83df867bf499b9283c8af778fa1168-2969862498724734806.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('957f93df-205e-42b7-8aa8-a12c24bfacaf', '55f57485-6faf-4059-84c4-cb18afffcff3', 'IMAGE', 'https://cdn.chotot.com/qu13FVf72jdl6FvpXAaVSCcV6evEZu-bFPIGx5sk3uo/preset:view/plain/c2be1955691a520a729a5ca79db83fd4-2969862498928986448.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('aed17307-521a-47bc-b9da-d17250214e62', '55f57485-6faf-4059-84c4-cb18afffcff3', 'IMAGE', 'https://cdn.chotot.com/WaCuKBbBJDHv-fD4ma0nWkTuD7Pv0k_zVyYBoBDWdIg/preset:view/plain/c8fa5891e4eba11bfe2e3b036d5d0f95-2969862498916429466.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('1d3d9228-ea0b-43cb-aaa8-af8aecf68eb0', 'P_133899247', 'APARTMENT', 'SIÊU PHẨM BAN CÔNG TÁCH BẾP CỰC PHẨM GẦN PHÚ NHUẬN', 'Dự án: 
Thông tin chi tiết: Cho thuê căn hộ mini đầy đủ tiện ích nội thất cao cấp , ban công thoáng mát . Gần trung tâm hẻm lớn Khu an ninh yên tĩnh . Hổ trợ xem phòng *** .', 'AVAILABLE', 'Quận Tân Bình, Tp Hồ Chí Minh', 40, 7500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4f8451aa-d74a-4e14-97b7-c17b196e8792', '1d3d9228-ea0b-43cb-aaa8-af8aecf68eb0', 'IMAGE', 'https://cdn.chotot.com/hMEB2d3RWW_UNaKVd88QIw_gnczeLcyNyB6rTPqZQcY/preset:view/plain/1c95ff61af405a1a4d76ed6d5c7f4914-2995789886308468196.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c6e13a9f-d47e-4315-84de-e9408e2c7616', '1d3d9228-ea0b-43cb-aaa8-af8aecf68eb0', 'IMAGE', 'https://cdn.chotot.com/wNZZiQb99sxZY1zCHl9yvFzgeg2o9eSedpZk7Jr2fYw/preset:view/plain/fd7cc7ec7b26437415faf9040e38ef72-2995789886351296889.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cc8a68fa-946b-4bd7-a793-02c4914407b8', '1d3d9228-ea0b-43cb-aaa8-af8aecf68eb0', 'IMAGE', 'https://cdn.chotot.com/tSQFyZ0WRGXN4Zt6eLO1ls0X2qkIB0-VM5pAflXe3qk/preset:view/plain/d8af454bef5758476e053af9cb7b88bc-2995789886362880682.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('717e02cb-72a9-48f7-b8fb-852467117221', '1d3d9228-ea0b-43cb-aaa8-af8aecf68eb0', 'IMAGE', 'https://cdn.chotot.com/mwJoEu-1NlEIswMR4L_e20rxq5K77tTlmTwhwxC5GhU/preset:view/plain/225ef45af4997853326804b1df2d666e-2995789886513756962.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b0171542-6394-4b8b-8bf6-d5af503e2b40', '1d3d9228-ea0b-43cb-aaa8-af8aecf68eb0', 'IMAGE', 'https://cdn.chotot.com/935dIJ9YGI4iPGJ7IhcP0K7HxI3eCJih0a8gGoeKj3Y/preset:view/plain/7aeacdf60a6be02be8cced69e15cac21-2995789886614084161.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('59307972-b2d1-42ac-83d5-346f8f609dde', '1d3d9228-ea0b-43cb-aaa8-af8aecf68eb0', 'IMAGE', 'https://cdn.chotot.com/nVkDr0YJYAbD7-GyEkM8LB20CTBj3dumHCePVEou5OQ/preset:view/plain/814aec9db375f2f0882bdbd08156b0ad-2995789886435546111.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('79e95899-1021-4be9-8a1d-6779ecc3aa42', '1d3d9228-ea0b-43cb-aaa8-af8aecf68eb0', 'IMAGE', 'https://cdn.chotot.com/lmeNqoq6991EFgDKCya7fS4l4Pr3C5H6hyq4W1NIE8o/preset:view/plain/20f313cf1cc57fd8b28eba3b18c9eaab-2995789886454237780.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b58efc89-76dc-4272-98b8-5478b3b73edd', '1d3d9228-ea0b-43cb-aaa8-af8aecf68eb0', 'IMAGE', 'https://cdn.chotot.com/eSqLKVswUubBV3QksNKinz9Jp2AX9bs5hVHr4RPv9_g/preset:view/plain/6a679d091e6d69fa589e2f8b7b085e4d-2995789886530936957.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('663df240-f3a7-4539-a2dd-a11d18740105', '1d3d9228-ea0b-43cb-aaa8-af8aecf68eb0', 'IMAGE', 'https://cdn.chotot.com/UsaQJWeZfz-YAGtsuOmnb1Wxk5oOUtBWaQ8TsGTYw_o/preset:view/plain/d25409d067e4ebe3fe365012d84fb20c-2995789887638014634.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('81e8e007-45dd-4bc7-9541-c3eacbacad99', 'P_133412511', 'APARTMENT', '🔥Nguyễn Trọng Tuyển - Căn Hộ Bancol/Cửa Sổ Thoáng Full Nội Thất Giá Rẻ', 'Dự án: 
Thông tin chi tiết: Tiện ích toà nhà:

+ Toà nhà với nhiều tiện ích chung, có người lau dọn hành lang bãi xe khu vực chung, có khu giặt

+ Phòng được trang bị đầy đủ nội thất gồm: Máy lạnh. Tủ lạnh. Giuong nệm. Tủ quần áo. Kệ bếp. Tủ bếp.,...

+ Hầm xe toà nhà rộng rãi, ra vào đi lại tự do, camera bãi xe hàng lang 24/7, trang bị pccc đảm bảo an ninh.

+ Khu dân trí cao an ninh, gần các cửa hàng tiện lợi, trung tâm mua sắm, khu sân bay, BV Tâm Anh,...

+ Thuận tiện di chuyển đi các địa điểm: CV Hoàng Văn Thụ, Vòng Xoay Phạm Văn Đồng, Vòng xoay Lăng Cha Cả, Dễ đi Quận 1 - Quận 3 - Quận 10 - Phú Nhuận - Gò Vấp - Binh Tân,...

Liên hệ: SĐT - Zalo - FB (Thái Thịnh).

Hỗ trợ tìm phòng và xem phòng khu vực Sài Gòn', 'AVAILABLE', 'Quận Phú Nhuận, Tp Hồ Chí Minh', 35, 4500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e29237cc-512c-4834-9fc5-1860d4d4462c', '81e8e007-45dd-4bc7-9541-c3eacbacad99', 'IMAGE', 'https://cdn.chotot.com/mm_wnSs_UVk4cUq-hgrUuiAyXIkgqJoteq-2BFZn_-w/preset:view/plain/f7cd9559798abfc283cd9a874880ad9d-2996019646740943871.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f4be680f-107c-44bd-bcc1-ef24ba5d8b4f', '81e8e007-45dd-4bc7-9541-c3eacbacad99', 'IMAGE', 'https://cdn.chotot.com/2xraFELZUT9dG3XS4ii4iSOaCCmk6xP3V-DqqfngH8g/preset:view/plain/1bd2528781793ba7941cea6422d2b30c-2996019647080740201.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('74366cef-4a3c-432d-b304-d8ce58497539', '81e8e007-45dd-4bc7-9541-c3eacbacad99', 'IMAGE', 'https://cdn.chotot.com/rR8YZY8ld1ZaylNqEgvLbtRlfLzAgr4XYd1kBRjkTy4/preset:view/plain/93a77a59cff8eaa961f384d4e07e3cdc-2996019647457734847.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9db16c4d-ccb9-482d-915a-721c89cfc5cb', '81e8e007-45dd-4bc7-9541-c3eacbacad99', 'IMAGE', 'https://cdn.chotot.com/j4k0d78v3Ti4OJ3RoJwEsL5y5lL2luTeQImxxhd1XXc/preset:view/plain/6042d7cc31674a994d9f116a15e42f7e-2996019648811943396.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f4a41b88-220c-42f6-8eab-abf2be0cd3da', '81e8e007-45dd-4bc7-9541-c3eacbacad99', 'IMAGE', 'https://cdn.chotot.com/EZiqPp5yS3aFR-ApwDRZlTrPfP4Nf-sYhvVfh2aRdpw/preset:view/plain/530d9734d6ca8ff306909258c1a7862a-2996019649140705657.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('860c0864-99f4-40e3-a417-febe127fad33', '81e8e007-45dd-4bc7-9541-c3eacbacad99', 'IMAGE', 'https://cdn.chotot.com/42R0LmcF1wRUejrH8cAV86KzJR4I8mg5prytS-28dsw/preset:view/plain/bba42776a510df6beb5a8099c38ee6f0-2996019649188750952.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('edfe6d65-9c93-447c-aaa0-8d388a1bf72d', '81e8e007-45dd-4bc7-9541-c3eacbacad99', 'IMAGE', 'https://cdn.chotot.com/sObttpKXhDSCAfkKXUACPlKcWZSoOQ_ww0wBjvKA-3M/preset:view/plain/6e78ef1bd7f33483ffb1d7a4e485e897-2996019649161180521.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cfc7a9d4-b56c-486d-981f-307d188da118', '81e8e007-45dd-4bc7-9541-c3eacbacad99', 'IMAGE', 'https://cdn.chotot.com/PBlvL76cCvqMv2NPMrDUARLwfh_xZLOEsvUGH3oD6Bk/preset:view/plain/4f69cae821d0339c74e72012267ef5d6-2996019649777782759.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('969afedf-5a16-45bd-bf1b-90eb4762ae3d', '81e8e007-45dd-4bc7-9541-c3eacbacad99', 'IMAGE', 'https://cdn.chotot.com/05h3_qC8LczuJ1JoiRGY-4113kTfIx9dpAd4Ykcu78Y/preset:view/plain/017afc8c70f8e6755b8474f6288f4b24-2996019649911903231.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1b59b70c-4f1d-473f-afe5-1bd0ac4d9b9a', '81e8e007-45dd-4bc7-9541-c3eacbacad99', 'IMAGE', 'https://cdn.chotot.com/-B4Mk1Ymqpu5qaBh8TETuAV33jE_yzINhypT-RKFJkU/preset:view/plain/4e2fd102760c6c5dfac141967be73b99-2996019649823387839.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c183d1fa-219d-4738-89dd-54a7e678c6e2', '81e8e007-45dd-4bc7-9541-c3eacbacad99', 'IMAGE', 'https://cdn.chotot.com/zC4P_0iRwEJy10dutbqELemF7mezRl71iRY_3DmIXJQ/preset:view/plain/83133e71dbebc5728283d57503d13d40-2996019649851099732.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('60dc61da-426f-4159-a7e1-3707a1f15d84', 'P_133940820', 'APARTMENT', 'Cho thuê Căn hộ Ngọc Lan khu biệt thự Tấn Trường 52m², 1pn/8tr/th', 'Cần cho thuê căn hộ Ngọc Lan, P. Phú Thuận, Q. 7, ngay khu biệt thự Tấn Trường, siêu thị, hồ bơi, lầu cao, view đẹp, ban công rộng, diện tích 52m², 1 phòng ngủ, 1 toilet, nhà có nội thất đầy đủ, ở ngay, giá thuê 8tr/th.
Liên hệ xem nhà 24/7', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 52, 8000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e6631525-f87a-461f-a52e-460dbb66e926', '60dc61da-426f-4159-a7e1-3707a1f15d84', 'IMAGE', 'https://cdn.chotot.com/J9prHoSMnpzyNllMqewx5zV3rhCLzIBCghfnqKcjrHE/preset:view/plain/935725d0ac43601032edfd9da2ec3846-2996122572717050233.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('12978529-72e7-40bb-944a-ccf00854bfbb', '60dc61da-426f-4159-a7e1-3707a1f15d84', 'IMAGE', 'https://cdn.chotot.com/wiAD24SAWwkPYi6OvM6yp0PR7Mrk10HRKiMygU_QdYk/preset:view/plain/99ee5af3e785a29fa9ae119aac9c1bd0-2996122582261602457.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b614b778-e8fd-4981-af9a-c7dbcb275543', '60dc61da-426f-4159-a7e1-3707a1f15d84', 'IMAGE', 'https://cdn.chotot.com/NMQyWx_5zm1-f3w7LdJOGQtwBlzZX-a_7GG9DeswI3A/preset:view/plain/9618ea5fbd4952d6a04908e2bfad8769-2996122594086331428.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a3905170-f404-42af-96ae-44cdabe281be', '60dc61da-426f-4159-a7e1-3707a1f15d84', 'IMAGE', 'https://cdn.chotot.com/ejN51MzQ0RanbyQr27nTPLCeOqW3iAQdk0ofLqvBpog/preset:view/plain/1b88084495d0d76d5ccb6191a129e8bf-2996122602072032740.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9833d7be-d006-45ff-a41c-6b1671322fa6', '60dc61da-426f-4159-a7e1-3707a1f15d84', 'IMAGE', 'https://cdn.chotot.com/NFxH6Lx2oZCjqx0xGeBzKsjCKKqwprS22sccQz5Qkas/preset:view/plain/99809e5c2393929b722fadd45ac66adc-2996122611338856825.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6a1fc28f-334d-4ed2-9ee2-b429516b2bdf', '60dc61da-426f-4159-a7e1-3707a1f15d84', 'IMAGE', 'https://cdn.chotot.com/HzOegsFRgJSCuwt0rRB9wvu9c2hlmV05HHxyddxcFB8/preset:view/plain/917ce4d5cd97bc1e9c0447e78a7736f0-2996122630577112548.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('c0653214-3218-4626-9328-b3f07ad53078', 'P_133494095', 'APARTMENT', '✨ SIÊU PHẨM Căn Hộ Mới Tinh ngay Nhà Thờ Phaolo - Cửa sổ Trời', 'Dự án: 
Thông tin chi tiết: Vị trí : Gần Aeon mall Bình Tân. Thuận tiện di chuyển sang các quận trung tâm, Bến xe miền tây, đường số 7, Vành Đai Trong, Kinh Dương Vương, An Dương Vương, Bà Hom, v.v.

🌟 TIỆN ÍCH NỔI BẬT 
- Thang máy di chuyển thuận tiện
- Trống sẵn phòng cửa sổ trời (3tr7) và phòng cửa sổ hành lang (3tr4)
- Toilet riêng trong phòng: Thiết bị vệ sinh hiện đại, sạch sẽ, có sẵn vòi xịt, gương soi.
- Giờ giấc tự do, không chung chủ
- Khóa cửa vân tay an toàn tuyệt đối.
- Hệ thống camera an ninh góc rộng, hoạt động 24/7.

📞 Liên hệ em hỗ trợ tư vấn nhanh chóng & xem phòng miễn phí', 'UNDER_OFFER', 'Quận Bình Tân, Tp Hồ Chí Minh', 25, 3400000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fbe0c883-8479-4edf-a1f4-89648444e0f5', 'c0653214-3218-4626-9328-b3f07ad53078', 'IMAGE', 'https://cdn.chotot.com/KsyNN5KxDPmeiO-CeVl4sh-x9TirhlwEcb_4xrdjczs/preset:view/plain/45f406d9af334d5960490bdbb5b87371-2992687072257458231.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d4d21dda-e719-4476-9836-e00ce75ae880', 'c0653214-3218-4626-9328-b3f07ad53078', 'IMAGE', 'https://cdn.chotot.com/QZa8YiB70O4iWmAw363naSD23vEDDlggqTuupvsqSm0/preset:view/plain/d12da6a48e50deb3b73bb486992eec22-2992687072234042893.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('eaa19c7e-4574-450d-a67a-242c4857ea78', 'c0653214-3218-4626-9328-b3f07ad53078', 'IMAGE', 'https://cdn.chotot.com/5pwvGONmzg_PlBJER8EqzOzYZ3kh91AFe3X6Cr4qEMI/preset:view/plain/7ea30891e7175c7c731e81d34d28ebcd-2992687072387200967.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2666eb80-799e-4819-9e0f-f222353e5ef8', 'c0653214-3218-4626-9328-b3f07ad53078', 'IMAGE', 'https://cdn.chotot.com/NBUoBEmttYgvdxnjh9RSt-MkaQgmAUa2K2QONY8r1Wc/preset:view/plain/986606a19b205d7ad75b58c4f0c053b6-2992687072477084568.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('978b6455-a87f-48a3-ab0c-d9ba3812b337', 'c0653214-3218-4626-9328-b3f07ad53078', 'IMAGE', 'https://cdn.chotot.com/ypCAbrQGIgHZY_BNzUzrMJAKKXh3v0YGjN9LZWpYWjI/preset:view/plain/05e90f0a427b328e8a4d3ff951851f02-2992687072527128559.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('67603ad5-f43f-4073-9f88-701bfd9fc416', 'c0653214-3218-4626-9328-b3f07ad53078', 'IMAGE', 'https://cdn.chotot.com/fjYIaahlBqToslIyPz8IeqnlKLPy9HndV5nBAMbPRQE/preset:view/plain/3d2f6f8d90ff5a61fa379f8eb62c956f-2992687072546041717.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('208e0e0c-e015-4d00-83d0-b5dff097f327', 'c0653214-3218-4626-9328-b3f07ad53078', 'IMAGE', 'https://cdn.chotot.com/IyJurCLurcQ-QGDF_elIazcSWQC3RKkX_MgVliBu9nQ/preset:view/plain/9a111948141e6e1be53f7f259ebe97fd-2992687072687829229.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0939a464-5391-4315-a9b7-e28af34e93fd', 'c0653214-3218-4626-9328-b3f07ad53078', 'IMAGE', 'https://cdn.chotot.com/w7zSIP3wwphGC5RPSZSjJYdJi0slqjoj615ZjSgEx_c/preset:view/plain/66bc0af5325d28cd1f7232be4f09fb4d-2992687072828423316.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('76c6411a-d863-4f6c-8f8e-e5a033d886fe', 'c0653214-3218-4626-9328-b3f07ad53078', 'IMAGE', 'https://cdn.chotot.com/Ys_mvRhzjTQfTcl5h5_u0RZus5775XBEtT1ggLzzC_s/preset:view/plain/369dd9d76592ac0f0d31153215514e34-2992687073180270647.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('63a51341-6cde-4000-8133-ea1b622edcec', 'c0653214-3218-4626-9328-b3f07ad53078', 'IMAGE', 'https://cdn.chotot.com/jVFcTaf94eAuFSHc1iz6uJkvQb38-XX3nVJHz7kWvhM/preset:view/plain/4c9c952651f471ecacc020a27dcdbd28-2992687073209350087.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('877e9f4c-0e20-4722-bf74-fc6d8e804223', 'c0653214-3218-4626-9328-b3f07ad53078', 'IMAGE', 'https://cdn.chotot.com/gbUcIkKwpmtML47JFxEVI2c0wlyxNPb81Dli548-ne4/preset:view/plain/4b72ee7912f85ba889ff5981d7f14816-2992687073173632525.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('dd57c6e2-f721-4b59-8f7c-d583b63d1d3b', 'P_133940798', 'APARTMENT', 'KHAI TRƯƠNG DỰ ÁN MỚI XÂY 100% NGAY ĐẦM SEN , ĐẠI HỌC HỒNG BÀNG', 'Dự án: 
Thông tin chi tiết: ✅Ngay ĐH Hồng Bàng

✨ Nhà xe rộng rãi - Ra vào vân tay - Giờ giấc tự do , ban công thoáng nhiều ánh sáng , thang máy
✨KHÔNG CHUNG CHỦ

✨ KHU DÂN CƯ AN NINH , ĐẦY ĐỦ TIỆN ÍCH

➖➖➖➖➖➖➖➖ 
🌱 𝐇𝐨̂̃ 𝐭𝐫𝐨̛̣ 𝐭𝐢̀𝐦 𝐯𝐚̀ 𝐜𝐡𝐨 𝐭𝐡𝐮𝐞̂ 𝐜𝐚̆𝐧 𝐡𝐨̣̂ 𝐝𝐢̣𝐜𝐡 𝐯𝐮̣ 𝐓𝐏.𝐇𝐂𝐌
 Đa dạng loại phòng: 𝗦𝘁𝘂𝗱𝗶𝗼 – 𝗗𝘂𝗽𝗹𝗲𝘅 – 𝟭𝗣𝗡 – 𝟮𝗣𝗡

🌱 𝐓𝐢̀𝐦 𝐏𝐡𝐨̀𝐧𝐠 𝐌𝐢𝐞̂̃𝐧 𝐏𝐡𝐢́ - 𝐋𝐢𝐞̂𝐧 𝐇𝐞̣̂:', 'UNDER_OFFER', 'Quận Tân Phú, Tp Hồ Chí Minh', 30, 5000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2ded3e38-a770-4016-87aa-b9581c92695f', 'dd57c6e2-f721-4b59-8f7c-d583b63d1d3b', 'IMAGE', 'https://cdn.chotot.com/8fgy6F_vfB_Xaa_ryumLWkdy8XpoWYDB-HbuhaQ1VnI/preset:view/plain/a4defbeb638347b38f9d97bacb8cb19f-2996122437373020537.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('370509f4-382c-4e1f-9bdb-adb4ff66cc63', 'dd57c6e2-f721-4b59-8f7c-d583b63d1d3b', 'IMAGE', 'https://cdn.chotot.com/fZJwRXG5DQxXfqFp-h-bY839yJVRz4k-PO19sMshrIw/preset:view/plain/f58e53cd526ebbc816cf5504f86d2d46-2996122437573449881.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0758e3c0-f3be-427c-ad6b-120d91cca70d', 'dd57c6e2-f721-4b59-8f7c-d583b63d1d3b', 'IMAGE', 'https://cdn.chotot.com/NlVJ64cBbp18xKNjmwjbDDBj-HZBODtq5hg1WfQDdVM/preset:view/plain/e616f2ffffa4c27fb428a4a55a96408c-2996122437541121639.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7f2d16e1-1c32-4cf4-8a13-b3cca7fa4719', 'dd57c6e2-f721-4b59-8f7c-d583b63d1d3b', 'IMAGE', 'https://cdn.chotot.com/NNabjOENu5mPFS6ihHn1A13XyMnJeEtxM0s0QT_UAWM/preset:view/plain/88d25cdccc790f10ec479e49dc90c579-2996122437634236504.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d53b1711-29be-491a-9870-2986315f3647', 'dd57c6e2-f721-4b59-8f7c-d583b63d1d3b', 'IMAGE', 'https://cdn.chotot.com/_XEluPY_NCZNOMDkOlTSo4wvksK_7dsKZCLGW1-pVwk/preset:view/plain/68ef45965fe4e73a1def545954130280-2996122437879583743.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dbb3c52d-f7bc-4bf3-a46f-32c30ce10631', 'dd57c6e2-f721-4b59-8f7c-d583b63d1d3b', 'IMAGE', 'https://cdn.chotot.com/kEvABZi6RLCwx9n4rwSv_VmH0csXSKJQoABszL-bgJ0/preset:view/plain/a426806119331a054fc3e7413c16e43d-2996122437655741319.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2f6869ef-cb9a-48c6-ace7-4de37af9ee89', 'dd57c6e2-f721-4b59-8f7c-d583b63d1d3b', 'IMAGE', 'https://cdn.chotot.com/0JIimCIwBX2KegaPqfyorUaonq-HSZN9iOpewIJ2U0Y/preset:view/plain/34d83454acdb2b0572ac62360c83329b-2996122437714744616.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('07744f6a-f897-4258-a825-12fc1aa9f62e', 'P_133940796', 'APARTMENT', 'CHO THUÊ CĂN HỘ DỊCH VỤ TỐT🏠Full nội thất🌷RỘNG-THOÁNG🌈ÍT CHI PHÍ✅', 'Dự án: 
Thông tin chi tiết: Trống Căn hộ CAO CẤP- SIÊU TIỆN ÍCH- Ngay Trung tâm Quận 2- ĐÁNG SỐNG ✨

📍Trần Não, An Khánh, Quận 2
- Vị trí kết nối Trung tâm Quận 1, Bình Thạnh, Gần Metro, Khu Sala, Thủ Thiêm, Ba Son,…
- Phòng đầy đủ nội thất cao cấp
- Bảo vệ, lễ tân, camera 24/7
- Hầm xe, thang máy, PCCC an toàn
- Dân cư văn minh, yên tĩnh
- Chỉ tính phí điện nước
Nước uống, Internet, Cáp,…', 'AVAILABLE', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 38, 6000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f053cc4f-93b0-4827-9a9e-d86b7a83c0bb', '07744f6a-f897-4258-a825-12fc1aa9f62e', 'IMAGE', 'https://cdn.chotot.com/_Ld3UoMBAxcgFV4QOrtYXUR_ADbnNbfc1OmcuUKF_80/preset:view/plain/07ba7ba6979806562c5c3e58d689b55e-2996122305830110692.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fbb43867-474e-49c8-b208-576aeae2a179', '07744f6a-f897-4258-a825-12fc1aa9f62e', 'IMAGE', 'https://cdn.chotot.com/1SC3UNSByhpQ_1U_KwL7slJsNu9KWN0bM1wMjYCVI34/preset:view/plain/1aeeaabc638ff5680c14e1aa448a2eb1-2996122305972162151.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f3719db9-2b6b-4e63-9d4b-1d49b6a48697', '07744f6a-f897-4258-a825-12fc1aa9f62e', 'IMAGE', 'https://cdn.chotot.com/5Tcqjyh6ohMLmv33ywQuRqFjov3zLqAMVyWHXNObde4/preset:view/plain/d42ca9a4b4be276ec247cc6279a577fd-2996122306010310310.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bc227617-d801-4712-9e84-842581ec33b5', '07744f6a-f897-4258-a825-12fc1aa9f62e', 'IMAGE', 'https://cdn.chotot.com/DOv9l9SaqSlZiWICs9yYECIz91jUSotNEhetc5SCUp8/preset:view/plain/7037cc74ac7b9c3afbb27209f40f9568-2996122306083102808.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('45750ca1-218c-497c-b9e2-e9ed34908ea2', '07744f6a-f897-4258-a825-12fc1aa9f62e', 'IMAGE', 'https://cdn.chotot.com/Q5WDQRaOrn_oNFcaxiPkSzeCuSc5aztnpILdOCwuKAY/preset:view/plain/44fb89ecb3b87a8f1278cb0e5fb1761d-2996122306038860853.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('42b75148-fbc9-4064-8b84-f6281f4d29ba', '07744f6a-f897-4258-a825-12fc1aa9f62e', 'IMAGE', 'https://cdn.chotot.com/0av4aS1iwDywCCLke3cmx3M6dfQlAmzl2802KHgDHzg/preset:view/plain/b91d00bd6f72b8316c4230dbb530c1d5-2996122306046433361.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('db9c0cbe-6347-4471-84cf-b71c2606ff47', '07744f6a-f897-4258-a825-12fc1aa9f62e', 'IMAGE', 'https://cdn.chotot.com/tfxo_JlnLjuEA8U9bDYvwip9MfXVdkBKo2kl1TlnSIg/preset:view/plain/3715e1618d4d147070d72f13ec65a38d-2996122306102704877.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b71c12a3-34bf-4cea-8ba7-027b4cf821ab', '07744f6a-f897-4258-a825-12fc1aa9f62e', 'IMAGE', 'https://cdn.chotot.com/vktgPuN3dreEtcfQCwdo9JClEPdtGVUYS9p0aXEoFHQ/preset:view/plain/e7aee0caea6278e2d2d046deb149fccc-2996122306114131240.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('83ebe36b-33a1-4f28-8cd1-633d9cbcc788', 'P_133940547', 'APARTMENT', 'Chính chủ 2 căn Vinhomes Grand Park bán cho khách cần đầu tư lâu dài.', 'Dự án: 
Thông tin chi tiết: Chính chủ sẵn 2 căn bán cho khách cần đầu tư lâu dài. 
Thiện chí khách thương lượng
Mua đầu tư 2 căn có giá tốt 
Bao trọn gói thuế phí tháng này', 'AVAILABLE', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 46.2, 2850000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6ea2f0bd-7cdc-449e-bab7-5f081507327f', '83ebe36b-33a1-4f28-8cd1-633d9cbcc788', 'IMAGE', 'https://cdn.chotot.com/e-INjhMMWe0G2RVbZHZjGF8nLPR_tvkKjMj7HEXaso8/preset:view/plain/244b679a79456cb570fe4167b01891cf-2996121561610599149.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4d5631d0-4102-4b70-8d2d-ed0e40957688', '83ebe36b-33a1-4f28-8cd1-633d9cbcc788', 'IMAGE', 'https://cdn.chotot.com/0xVfEtq9TCf8rEkuAcdvlZZBzKGJu-s5byQ2ciwK9lM/preset:view/plain/f6ff2febfc9701daf5eebc84b5d94b1b-2996121561555245137.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('218b2ad5-4f22-4b83-8a32-4a55464ef2d8', '83ebe36b-33a1-4f28-8cd1-633d9cbcc788', 'IMAGE', 'https://cdn.chotot.com/D22ABj9nXJNPN1PpQhfpmLnQX-FzWnLSJf_eZKTyX_Q/preset:view/plain/304287fea3fc1f79690dd251ae63eb29-2996121561050489892.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5222f22d-1cf3-45fa-af24-ac31e3639f57', '83ebe36b-33a1-4f28-8cd1-633d9cbcc788', 'IMAGE', 'https://cdn.chotot.com/MYnGWBIMV6cYNUhPpWSh52KOxBO9419Q0EzXAaWOzHM/preset:view/plain/d192e85cda1d09d01a8258f09929376f-2996121561315726335.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3fa8137e-ca00-49a9-9ed3-84e7b7ce94bb', '83ebe36b-33a1-4f28-8cd1-633d9cbcc788', 'IMAGE', 'https://cdn.chotot.com/WhvLrIumtD6SbUmLMIVbzmJj0ZOsnQKXE7nNTBmFHGk/preset:view/plain/ca736836182629e3a023e28e9624602a-2996121559907387769.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c96a834a-b3cd-4a05-ba9e-9e373da72384', '83ebe36b-33a1-4f28-8cd1-633d9cbcc788', 'IMAGE', 'https://cdn.chotot.com/LBji190kKpeUonHs6HdGC_2B3JIy-de0rru_Aws-5kU/preset:view/plain/6aaa12f369e78ca4284183043066c34c-2996121560936095832.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8d9b4931-1aed-4b52-b135-a5d59ab96d05', '83ebe36b-33a1-4f28-8cd1-633d9cbcc788', 'IMAGE', 'https://cdn.chotot.com/Uq1gEoUy3tGsII--HVN0uoRKsDPncwR3lciiMUxkmN8/preset:view/plain/2bf180b8eb8339faadf4d58dfc08cf74-2996121560923489764.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('8bb46c6c-08e4-40ab-a742-2e5b313256f2', 'P_133940787', 'APARTMENT', 'CHO THUÊ CHUNG CƯ CENTRAL GARDEN - 80M2 - 2PN 2WC - GIÁ 17 TR', 'Diện tích: 80m²

Kết cấu: 2 phòng ngủ, 2 phòng vệ sinh, thiết kế hiện đại, các phòng đều đón ánh sáng tự nhiên thông thoáng.

Giá cho thuê: 17 triệu/tháng.

Ưu Điểm Nổi Bật
Vị trí trung tâm: Tọa lạc ngay vị trí chiến lược, kết nối nhanh chóng sang các quận trung tâm thành phố và các tuyến đường huyết mạch.

Tiện ích giáo dục: Nằm gần nhiều trường đại học lớn, cực kỳ thuận tiện cho sinh viên, giảng viên hoặc gia đình có con em đang theo học tại khu vực trung tâm.

Tiện ích nội khu: Tòa nhà an ninh 24/7, hầm để xe rộng rãi, xung quanh ngập tràn tiện ích như siêu thị, chợ, cửa hàng tiện lợi và các dịch vụ thiết yếu khác.

Liên Hệ Xem Nhà
Họ và tên / SĐT: ***

Hỗ trợ xem nhà thực tế nhanh chóng, pháp lý rõ ràng, thương lượng trực tiếp chính chủ.', 'SOLD', 'Quận 1, Tp Hồ Chí Minh', 80, 17000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('facbfd73-a1cb-483a-9a3a-9f3abf1388a1', '8bb46c6c-08e4-40ab-a742-2e5b313256f2', 'IMAGE', 'https://cdn.chotot.com/P6b4xCXkMpf13BDR4Y0cTxqT8b7UghBnl9aDxWHIzTo/preset:view/plain/4782913e5cb20cbfc91948986080d2ee-2996122148656473766.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('87bb73b0-1c6b-4ae3-b6d7-6c75d1fbb31e', '8bb46c6c-08e4-40ab-a742-2e5b313256f2', 'IMAGE', 'https://cdn.chotot.com/OZmPXstA5sI97Bk2sh28aBD-E6Z6xRrRfYn1oHh3RMY/preset:view/plain/3a0e95ffe0283455fc26929f6f0596c1-2996122148684355449.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('94460da3-8b3b-4c70-a76c-784aa363c745', '8bb46c6c-08e4-40ab-a742-2e5b313256f2', 'IMAGE', 'https://cdn.chotot.com/B7z7f-ETaI2hYpYk0i5hv1dBU9ncf3pEccI2-bVcIDU/preset:view/plain/02b0a746948ea84e5075c982d59349d5-2996122148497082745.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('38d10bf9-be04-4de4-9619-0ed83aa72806', '8bb46c6c-08e4-40ab-a742-2e5b313256f2', 'IMAGE', 'https://cdn.chotot.com/E3ee3h6AZ-vx0HfhBRb32GQBQI9LFOVNepTAuqzrdnQ/preset:view/plain/d8a81bc40fc72296cb8329a33bd4ec14-2996122148684252039.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f024cb4f-aca6-4bc7-8018-803a7c2b67af', '8bb46c6c-08e4-40ab-a742-2e5b313256f2', 'IMAGE', 'https://cdn.chotot.com/GSJlAGat3nD8aLeszG26IYyWsvW2JlkF7DalAaSORQU/preset:view/plain/c2dd2f103f6a104acf731861cbc54435-2996122148626011432.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('b8e919ca-3676-4f18-84c5-11ed22839fa2', 'P_132802929', 'APARTMENT', 'Căn hộ Saigon Mia 3PN cho thuê giá 15tr/tháng, sẵn rèm máy lạnh', 'Căn hộ Saigon Mia 3PN cho thuê giá 15tr/tháng, sẵn rèm máy lạnh

- Thông tin:
+ Diện tích: 76m² - 3PN - 2WC.
+ Nội thất: Sẵn rèm, máy lạnh, máy nước nóng. IB em gửi hình chi tiết ạ!
+ Giá thuê: 15 triệu/ tháng.

Tiện ích:
- Hệ thống hồ bơi tràn bờ.
- Khu thương mại cao cấp.
- Khu ăn uống, quán cà phê.

Gọi em Ngọc đi xem nhà. Tư vấn nhiệt tình, tận tâm 24/7 !
Cảm ơn anh chị đã đọc tin!', 'AVAILABLE', 'Huyện Bình Chánh, Tp Hồ Chí Minh', 76, 15000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c10573ad-d90c-4482-9cde-4b5ab5c82c40', 'b8e919ca-3676-4f18-84c5-11ed22839fa2', 'IMAGE', 'https://cdn.chotot.com/UIU4C7oQPrc79R1awTq6lCElsUA0aJNfn1THq2YGkhk/preset:view/plain/128e8744b4521b0272811323cf2de1b8-2987425269610582600.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ecc8e91e-e3ad-49f8-863d-c03a6aafbbce', 'b8e919ca-3676-4f18-84c5-11ed22839fa2', 'IMAGE', 'https://cdn.chotot.com/GQ8gElRuCba3dpLZwP6J3zLYoQeuYWmxUKJHvDVNQmU/preset:view/plain/fc91ec6df3b3322f0a1adcb5f9746efd-2987425269560454918.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f29e7d02-a05b-416d-97ae-82c1ba3ea8f5', 'b8e919ca-3676-4f18-84c5-11ed22839fa2', 'IMAGE', 'https://cdn.chotot.com/k1NR73XgWtopJiHQCXyn38vDjeZtrAOHBeK-1b9pnlU/preset:view/plain/8acbf9aace442d221163da79a875f62b-2987425269646508733.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c7bc601c-ff6f-496a-8f88-4c6c493b8cce', 'b8e919ca-3676-4f18-84c5-11ed22839fa2', 'IMAGE', 'https://cdn.chotot.com/tSSRJ8cnrkxhCmAiVLvoq5wdsyaKYHGvPsCugCtfm8g/preset:view/plain/fd8bb890320b2adbed84c962c70f7907-2987425269554211535.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('497cf150-7c69-450d-847d-94596c70db68', 'P_133940773', 'APARTMENT', 'CĂN HỘ BANCOL FULL NỘI THẤT - PHẠM NGŨ LÃO GÒ VẤP', 'Dự án: 
Thông tin chi tiết: 🔥 SIÊU DEAL THÁNG NÀY – PHÒNG ĐẸP FULL NỘI THẤT GIÁ SỐC 🔥
📍Phạm Ngũ Lão, P.1, Gò Vấp
✨ Tiện ích nổi bật:
• Full nội thất cao cấp – xem phòng là mê
• Nhà có thang máy + thang bộ
• PCCC đạt chuẩn, camera an ninh 24/7
• Tự do giờ giấc, không chung chủ
• Chi phí rẻ: Điện 4k – Nước 100k – DV 200k
• Nhận tối đa 3 người / 2 xe', 'UNDER_OFFER', 'Quận Gò Vấp, Tp Hồ Chí Minh', 35, 5600000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7740e2a6-148d-475d-b545-9d168dbe7eb2', '497cf150-7c69-450d-847d-94596c70db68', 'IMAGE', 'https://cdn.chotot.com/FGvCUBX-AVlAogZoHrFxQj9VXvtzjq61Y2A1Bf0ck2w/preset:view/plain/1984c99a38d4a645d20afc4c2154bd0f-2996122503671432676.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('232d1ad1-69a3-4648-89b9-00cf6657f323', '497cf150-7c69-450d-847d-94596c70db68', 'IMAGE', 'https://cdn.chotot.com/GVwn5JnVXwouMSVwqDm4-tzRfwV8CWfM4eXrCQIbP6g/preset:view/plain/6c2198e8abf3634a023c3d265d092d88-2996122503739778084.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ae587e27-ef7d-49bc-b908-c2050eeebc64', '497cf150-7c69-450d-847d-94596c70db68', 'IMAGE', 'https://cdn.chotot.com/XDIkFHM7MVR9PQg8kL3M4nDdU55GyPVU4Zs6RmNWIdI/preset:view/plain/ba8f691154fc189aa01053a0c7ac957b-2996122504183337983.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f98c8ffd-0d77-4a7b-9148-2a4738f64abb', '497cf150-7c69-450d-847d-94596c70db68', 'IMAGE', 'https://cdn.chotot.com/vjQununUF_wi1ilOWrTIKlBwL5i9FjDe1G5hBPV8FCI/preset:view/plain/3084a4d052b2950d926fbab34189be0a-2996122503827003545.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('16cad6f8-47fc-4680-b187-66906a9f76c8', '497cf150-7c69-450d-847d-94596c70db68', 'IMAGE', 'https://cdn.chotot.com/mD_PXP255sAIHrRt8g0a6lV5d5nvO1cmSliF7NCjvT8/preset:view/plain/67f63fe8e6d0e1b8319553c9fb8bef3d-2996122503828491879.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cd16e30f-6813-4b9b-8e0e-76afbbfbd09b', '497cf150-7c69-450d-847d-94596c70db68', 'IMAGE', 'https://cdn.chotot.com/q1NGfFIeQdGk2lCmhwqYNNaGdfPXCwKO_-2udy2m5S0/preset:view/plain/7b3ac25d1445435d01ae7cb3090dcb5f-2996122503711115641.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('ef9d1165-d5a2-4ae2-a158-a83af5cb6b29', 'P_132985020', 'APARTMENT', 'Bán Gấp 2Pn 2Wc 66m2 Lovera Vista Sổ Hồng Sẳn Nhận Nhà Ngay', '❤️Chủ Thân Gửi Em Bán Gấp Căn Hộ Lovera Vista ❤️
☀️1Pn + 1 52m2 : 2.700.000.000 - 2.720.000.000
☀️2Pn 1Wc 54m2 Full NT : 2.750.000.000
☀️2Pn 2Wc 60m2 : 3.050.000.000
☀️2Pn 2wc 65m2 : 3.080.000.000
☀️3Pn 2wc 78 - 83m2 : 3.600.000.00***0
👉 Căn hộ đã có sổ dọn vào ở ngay
Giữ xe: 100 ngàn/xe. Điện - nước theo giá nhà nước. Miễn phí hồ bơi, gym, yoga...
Thông tin mô tả.
- Full tiện ích giữ xe, hồ bơi, công viên, siêu thị, sân cầu lông, bóng rổ, 711, bách hoá xanh, co.op food... Tại dự án.
- Dự án 1.310 căn hộ với 5 block cao 20 tầng.
- Nhà trẻ, trường tiểu học, THCS, THPT trong bán kính 1km.
🍀🍀🍀Là đơn vị chuyên chuyển nhượng tại Lovera Vista Chúng tôi cam kết hỗ trợ Bạn tìm được căn hộ ưng ý với giá cả hợp lý. Đặc biệt với chế độ hậu mãi đã làm hài lòng tất cả những Khách hàng từng làm việc với Chúng tôi.', 'AVAILABLE', 'Huyện Bình Chánh, Tp Hồ Chí Minh', 66, 3080000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('71795115-ecee-4aac-bdba-bc8c19cb7955', 'ef9d1165-d5a2-4ae2-a158-a83af5cb6b29', 'IMAGE', 'https://cdn.chotot.com/DBAd4lcCHqmDCePDnVp47yTKoLr0jpKBzOwEbtFbVG8/preset:view/plain/d2211b42d9382a00a223daad75b485d5-2988850280437098892.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d41c0dbe-0c32-45f6-aa76-f7c62cfaaa33', 'ef9d1165-d5a2-4ae2-a158-a83af5cb6b29', 'IMAGE', 'https://cdn.chotot.com/_KZCgqwWMe7HokueoSWhUC9cPRU05D5rIjVCq9sj1Ug/preset:view/plain/d109082b7ff5931228009c087951de79-2988850280746219367.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('139a1843-799a-440d-945e-f72b8a51f3ca', 'ef9d1165-d5a2-4ae2-a158-a83af5cb6b29', 'IMAGE', 'https://cdn.chotot.com/8vLS8r8GRllu7hRbQ15JlrW2z_2iJJ2VtqanrvL6fCg/preset:view/plain/5f6f71a6c346a4886d6f6898a7ec431c-2988850280699146064.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('104ffccb-321e-4816-8a1e-ae12712cadc8', 'ef9d1165-d5a2-4ae2-a158-a83af5cb6b29', 'IMAGE', 'https://cdn.chotot.com/0DLVD14qEzcQUfydlkA829bFTjfWOGeHt3BRIPJQwL4/preset:view/plain/9bd74ba160c8f219d33f3f54b9b6dfc5-2988850280751670976.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a002dd39-9daa-428a-887f-85fd061d42ff', 'ef9d1165-d5a2-4ae2-a158-a83af5cb6b29', 'IMAGE', 'https://cdn.chotot.com/hvM6Tdz80u2ANzB8Rc6S0iHbmAX1fG5KYZa7R99zpZ8/preset:view/plain/58cff4756a58dde3af3b49e82d49f745-2988850280969353076.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8719406e-4c37-46b9-970d-125f14393f16', 'ef9d1165-d5a2-4ae2-a158-a83af5cb6b29', 'IMAGE', 'https://cdn.chotot.com/5rQR2ZiV2tB1pP_crw-Zlj5YKq2tFnBPsnaE7MnNFK4/preset:view/plain/1ac13fd78f4329184e898610b7950aa2-2988850280831691125.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fc8af924-a9e5-4f16-af33-cc9c730ebf6b', 'ef9d1165-d5a2-4ae2-a158-a83af5cb6b29', 'IMAGE', 'https://cdn.chotot.com/FOAx2uizWD25OZ6dLulIlIwHwiiwl3dvCl7ZAI4ISIE/preset:view/plain/ee1e8e22c11c54cfd9c6835619695a56-2988850279055038347.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b1be8940-4316-4586-862b-0ec37add0205', 'ef9d1165-d5a2-4ae2-a158-a83af5cb6b29', 'IMAGE', 'https://cdn.chotot.com/7SSNdLOnnOiIJY0uvQ9okrS5-3v9Y5Xo57CfMge0uhc/preset:view/plain/281a2957406c2aa14df63d693a89b43a-2988850280533054380.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f27497f9-8cf8-4729-8c41-28af02f09a7a', 'ef9d1165-d5a2-4ae2-a158-a83af5cb6b29', 'IMAGE', 'https://cdn.chotot.com/zgOj-Wv0sLQSdH6S1HhaK9XSLBKurzMH8Tg-cbknHZ0/preset:view/plain/292fc6ce25bb6fd111e3392a540b8af3-2988850317850814860.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('851ad5e0-b12c-496a-aca4-698d136ac8e3', 'P_133940747', 'APARTMENT', 'Cần cho thuê chung cư Bảy Hiền diện tích 70m - 2PN GIÁ 12 Triệu ', 'CHO THUÊ CHUNG CƯ BẢY HIỀN TOWER, TÂN BÌNH

📍 Địa chỉ: 9 Phạm Phú Thứ, P. 11, Tân Bình
📐 Diện tích: 70m²
🛏️ 2 phòng ngủ
🚿 2 WC
💰 Giá thuê: 12 triệu/tháng
🛋️ Full nội thất
🔑 Nhận nhà ở liền

Căn hộ đầy đủ nội thất, thiết kế rộng rãi, thoáng mát, chỉ cần xách vali vào ở. Vị trí thuận tiện, gần chợ, trường học, siêu thị, sân bay Tân Sơn Nhất và dễ dàng di chuyển đến các quận trung tâm.

📞 Liên hệ xem nhà: Ngọc ', 'AVAILABLE', 'Quận Tân Bình, Tp Hồ Chí Minh', 70, 12000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('87f1c273-3cea-4548-a1e5-d8bdde3a3c0d', '851ad5e0-b12c-496a-aca4-698d136ac8e3', 'IMAGE', 'https://cdn.chotot.com/7gzod0L8kgI5sbhksUXN-hVrpc-qeWPQ3cLa9g-eEs0/preset:property_project_small/plain/1896_overview_1.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a8bd94ed-868f-4177-b3b3-06ce4464ae97', '851ad5e0-b12c-496a-aca4-698d136ac8e3', 'IMAGE', 'https://cdn.chotot.com/FRikFsdXZJ1wuYOkhESv9DVRXTqf0629PDiG6krXbkE/preset:property_project_small/plain/1896_overview_4.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7991ae7f-a7f9-4096-9bf6-60cfaa727df1', '851ad5e0-b12c-496a-aca4-698d136ac8e3', 'IMAGE', 'https://cdn.chotot.com/cp3WvRoLfv4TlCeka2AvL5Z0BPrI0TYwB5hot3gKtwg/preset:property_project_small/plain/1896_floor_plan_project_5.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('9562170d-02f1-4ca0-aaf4-657a9aea20f1', 'P_133940737', 'APARTMENT', 'CHÍNH CHỦ CHO THUÊ CĂN GIAI VIỆT', 'Chính chủ cần cho thuê căn giai việt có rèm ,máy lạnh... Căn hộ thoáng mát,phòng ngủ rộng rãi,khu vực an ninh,giao thông thuận tiện đi lại các quận,gần chợ,siêu thị.', 'SOLD', 'Quận 8, Tp Hồ Chí Minh', 82, 11500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2becd1f6-8ae4-4c38-9a72-00f90a557928', '9562170d-02f1-4ca0-aaf4-657a9aea20f1', 'IMAGE', 'https://cdn.chotot.com/fSrkeLXhB_Tq-77--wHvEYy3rSavlz4KQLafNsUEbQY/preset:property_project_small/plain/2972_overview_1.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1654bd95-54e0-4331-b7f3-758c5a6bf9bc', '9562170d-02f1-4ca0-aaf4-657a9aea20f1', 'IMAGE', 'https://cdn.chotot.com/yZQ-QRN2N06oK66RtU2wOm4hfDFbpfonjQds0yYZfwg/preset:property_project_small/plain/2972_sample_house_3.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d73fb732-fa80-4d97-b2f7-4a2d1224033d', '9562170d-02f1-4ca0-aaf4-657a9aea20f1', 'IMAGE', 'https://cdn.chotot.com/WB2Tp3WbZ6SfsIo0b-TJVZg00qVuxlJywC76BDTFioc/preset:property_project_small/plain/2972_floor_plan_project_5.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('63f99652-485d-4834-b8d5-f4850d36ee9b', 'P_133448517', 'APARTMENT', 'tầng trệt chung cư', 'Dự án: 
Thông tin chi tiết: Nhà trệt hẻm xe tai gan moi tien ích chợ truong sat ben', 'AVAILABLE', 'Quận 6, Tp Hồ Chí Minh', 60, 7000000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('524f59be-5c23-4e97-86ad-ede7dc4522c6', '63f99652-485d-4834-b8d5-f4850d36ee9b', 'IMAGE', 'https://cdn.chotot.com/MFa00UPYjK3DOBK0CeAzUfe1qF_EAuQIiIp_NQy-aEM/preset:view/plain/b6e1ac8c5e663291510cf30b4752aa9e-2992350243119494669.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4a462221-54cc-4b40-8609-39f378f64109', '63f99652-485d-4834-b8d5-f4850d36ee9b', 'IMAGE', 'https://cdn.chotot.com/Khvk4WpGKwneDNH7uC5LmF__pktulDnRnH-DfpLCJ2Q/preset:view/plain/308a094589ccec7ca94306130d290ff3-2992350243085502258.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('79e8c817-6051-491f-9dad-99fb8679c90c', '63f99652-485d-4834-b8d5-f4850d36ee9b', 'IMAGE', 'https://cdn.chotot.com/yviQ3IMXbAQ8X9ePxf2wsgXqruUP0jUsnm7Jf2uZBhY/preset:view/plain/084eb694e2dd0ab8068bdb8dd16b3ce7-2992350640888282278.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('c208d80a-ce8a-4623-b79c-368d5f6d7542', 'P_133696269', 'APARTMENT', 'Sang hợp đồng thuê căn Goldview 2pn 1wc đẹp chỉ 17.5tr/th, t8 ở dc', 'Dự án: 
Thông tin chi tiết: Kim cho thuê Goldview Q4 giỏ hàng nhiều căn xem nhanh ***', 'AVAILABLE', 'Quận 4, Tp Hồ Chí Minh', 70, 17500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('845b1227-2307-48a8-82d2-a19ab1686a1a', 'c208d80a-ce8a-4623-b79c-368d5f6d7542', 'IMAGE', 'https://cdn.chotot.com/_ENfT3ydYq2D3DgXGEFKqO1lTXeAf-PLA-hzuSw2QsY/preset:view/plain/0fe3d33a63d2ffd08dc9e74d9942f3c5-2994248988563544981.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5d7f5927-f34e-46a6-b632-35022913c7be', 'c208d80a-ce8a-4623-b79c-368d5f6d7542', 'IMAGE', 'https://cdn.chotot.com/SDeotjx9uaO5chYxDLeJC3qqZDf-ZD0wgz9P80lY_I0/preset:view/plain/c904079cd19047021780cd8265d19e0f-2994248988817663297.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('67644b5e-3322-45af-992d-580190f0613c', 'c208d80a-ce8a-4623-b79c-368d5f6d7542', 'IMAGE', 'https://cdn.chotot.com/4vv3QdEvJ2zLe6sc4Rl3De5D8-2ncP6YzJFIKV43aJg/preset:view/plain/507809afe1ecd21af4f844fa9f3be441-2994248988745212321.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0a2e6ce4-99ac-48b3-bcf3-5b4348ec3bb0', 'c208d80a-ce8a-4623-b79c-368d5f6d7542', 'IMAGE', 'https://cdn.chotot.com/ebjxmBexw0RveEImEADW7bEGPELiPF9g58QhnlW6Joo/preset:view/plain/6c4fb277be3e200013d1dd4c1ae0fb05-2994248988893771752.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1c8dfa89-a3d3-4a5a-b680-166c7a10acd8', 'c208d80a-ce8a-4623-b79c-368d5f6d7542', 'IMAGE', 'https://cdn.chotot.com/KjMBHEp-uFQraGJJGfqErzYNx1NpMKuWrjnucDMEmFw/preset:view/plain/0a746fca58f3e6fa6a88866d6e0f8181-2994248988956597445.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('70f723be-eb00-46d2-bfdb-10a2d2f14554', 'P_132747102', 'APARTMENT', 'DUPLEX Cao Cấp,Giặt Riêng,Thang Máy,Siu Thoáng,Ngay Cầu Chánh Hưng', '🍃CHDV CAO CẤP TẠI QUẬN 8 SIÊU XINH

Địa chỉ: Hưng Phú - Quận 8
❗️ MỚI TOANH
__________________________________
- Full nội thất
- Không chung chủ
- Giờ giấc tự do, an ninh
Gần cầu nguyễn tri phương,cầu chữ y,parc mall…
LH: (zalo/call) hỗ trợ xem phòng trực tiếp', 'SOLD', 'Quận 8, Tp Hồ Chí Minh', 25, 6800000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1b6f9922-fa44-48c8-9d3d-ad0eb3c54760', '70f723be-eb00-46d2-bfdb-10a2d2f14554', 'IMAGE', 'https://cdn.chotot.com/Tfx0PiP43IodFH20WpGfWjSrJFwxtuxwZTLrn6sNNjc/preset:view/plain/dadb28e58d97e1125bb4166c7b6f40c0-2995287159378203504.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('53420a44-564d-4369-8636-80144887bed0', '70f723be-eb00-46d2-bfdb-10a2d2f14554', 'IMAGE', 'https://cdn.chotot.com/5A0xt0oYgAgqX3nvy2sZHLN_hzkhBC8NUeaxgYiNRT0/preset:view/plain/0642e7c38c5b726cf4d32a391ca08021-2995287159593292170.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('287d5a0a-bbcd-4adb-b1af-fbdc345b73fc', '70f723be-eb00-46d2-bfdb-10a2d2f14554', 'IMAGE', 'https://cdn.chotot.com/EDV6dHNV_oNT7n4KFNu3UTyaJIuReM1h0cMItYJE9w0/preset:view/plain/c3a2fe7ce71dd703d0abba1e6efafd6a-2995287159567239545.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5a15c848-181e-46a1-bc92-7333e6cceb16', '70f723be-eb00-46d2-bfdb-10a2d2f14554', 'IMAGE', 'https://cdn.chotot.com/r00KrzZt3Qxcil_8cHz2YS5kJrZGPNerRMnRLo1KopE/preset:view/plain/ce1f045d27bdadd671845b6ce49a62c4-2995287159463047092.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6eb176c6-c0b9-4e59-a03d-3cac97918104', '70f723be-eb00-46d2-bfdb-10a2d2f14554', 'IMAGE', 'https://cdn.chotot.com/cDZmTjAHy01syRXxMCAW-40kK29OnncCjVT59kAovPs/preset:view/plain/a0f8e75af115f0c94f975e3e3610ab98-2995287159539180239.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6b6c1663-4713-4dd5-a303-75faa85321ca', '70f723be-eb00-46d2-bfdb-10a2d2f14554', 'IMAGE', 'https://cdn.chotot.com/c7vt16YyU1niYxTBx2PH8wN8GvZRviNvonhdM4owZHI/preset:view/plain/8b838f9e393227faf3b1001b112ff12b-2995287159688262448.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('20e38d9b-1361-407a-9385-ac5e68dc0e8c', '70f723be-eb00-46d2-bfdb-10a2d2f14554', 'IMAGE', 'https://cdn.chotot.com/8nSbospv7jRfHdczGQ2YIaN75n9oXePBmRWSpKRS9fI/preset:view/plain/e9e847f7f93e1607f38ed017b092cfba-2995287159597820926.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('eb060b9f-38ab-41f7-9d51-5a90f6478c61', '70f723be-eb00-46d2-bfdb-10a2d2f14554', 'IMAGE', 'https://cdn.chotot.com/TmcKUhf6CNEnHWT4expLgte4MYyJCQgyoEaG9wkkl1o/preset:view/plain/7899e678fd0d8df2dadf2efbc8d9679e-2995287159571892603.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e62e6aa7-04bf-4de9-bbeb-9ae981428033', '70f723be-eb00-46d2-bfdb-10a2d2f14554', 'IMAGE', 'https://cdn.chotot.com/NeaNqBbvSOEHq3yBpsmgqi14nixCt3P6iCoaHEFWzRE/preset:view/plain/3f6f4ad473b143dd1ea18905b68e5733-2995287159545599579.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1a5f6149-4f59-4f44-881d-79c7d3b89dc0', '70f723be-eb00-46d2-bfdb-10a2d2f14554', 'IMAGE', 'https://cdn.chotot.com/2tzpiH32me82tUv3jY98_9jzX010lCjNd0xYQaL2A0A/preset:view/plain/824905a685e3c715562b45a8dd09a5e7-2995287159576984095.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8c407a89-78af-4e24-9190-773bb8b059e8', '70f723be-eb00-46d2-bfdb-10a2d2f14554', 'IMAGE', 'https://cdn.chotot.com/9OuOIb33GGhrgAyLjvI5jb4qvFLyvgQ6NrZ7NYzHdvc/preset:view/plain/d73a3b7721c49d438a88880f433b7976-2995287159644500046.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('3777fa4d-0220-4494-89e1-6fdddd8ed2d4', 'P_133940704', 'APARTMENT', 'KHAI TRƯƠNG MỚI 100% CĂN HỘ 1PN TÁCH BẾP_ BẢO VỆ 24/24_YÊN TĨNH', 'Dự án: 
Thông tin chi tiết: CĂN HỘ 1PN GẦN CV HOÀNG VĂN THỤ - FULL NỘI THẤT - KHU VỰC YÊN TĨNH, AN NINH, DÂN TRÍ

📐 Diện tích: 42
🏠 Loại phòng: 1PN nhiều cửa sổ lớn - ban công
Tiện ích căn hộ
✔ Dọn phòng 2 lần/tuần, thay ga 2 lần/tháng.
✔ Căn hộ full nội thất
✔ Máy lạnh, tủ lạnh, máy giặt
✔ Bếp riêng, WC riêng
✔ Không chung chủ – giờ giấc tự do
✔ Khu an ninh, camera 24/7
Khu vực 
 • Trung tâm tài chính, văn phòng: Công an Thành Phố, rạp chiếu phim, toà Lancaster, Công viên 23/9, chợ Bến Thành, Metro Bến Thành.
 • Di chuyển cực kỳ thuận tiện di chuyển sang quận 3, quận 2, quận 1, quận 10,…

👉 Chuyên cho thuê căn hộ trung tâm TP.HCM đủ loại: 
🍀 Phòng trọ, căn hộ dịch vụ, chung cư 
🍀 Hỗ trợ tìm phòng và tư vấn miễn phí 
🍀 Đa dạng sản phẩm', 'UNDER_OFFER', 'Quận Phú Nhuận, Tp Hồ Chí Minh', 40, 8900000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a762ed37-1fb7-49a5-a2f7-ccb506e293be', '3777fa4d-0220-4494-89e1-6fdddd8ed2d4', 'IMAGE', 'https://cdn.chotot.com/G1CMdNVdmW4zUMi3AmrmSkaUT5CRoNrx-IB-3nBhfhM/preset:view/plain/507b6c4ed746a65efd4ea3dc7ee45bd8-2996121881586912871.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('876919b3-287b-4768-bbb1-2a6f84d26ff3', '3777fa4d-0220-4494-89e1-6fdddd8ed2d4', 'IMAGE', 'https://cdn.chotot.com/uE1Ocgx03IL-7xLmjQefdQySy-5Iu_fl9AvrlpAIQSc/preset:view/plain/824e41389dc6a967752280e5dc7b4530-2996121881649190184.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('26cc2422-5101-4c59-9d33-3f00fa8921a6', '3777fa4d-0220-4494-89e1-6fdddd8ed2d4', 'IMAGE', 'https://cdn.chotot.com/JW1Bz3YHd7s6xq3cNVWESLfZ8Auk1-QbJ6mz3ng1m3c/preset:view/plain/04ffcfa0309b24e24681018940ac8778-2996121881583503737.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('00762c16-1726-47bf-9cbc-45b4bf125c0f', '3777fa4d-0220-4494-89e1-6fdddd8ed2d4', 'IMAGE', 'https://cdn.chotot.com/eiXZdBI76uFKwCQp8Uiy4vmSlbciZJ8b5NnckY1s2vw/preset:view/plain/07a3d0807c834de938c8457a1b1c25fd-2996121881834660900.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('27acd840-9745-4c48-836b-f961ba40aad4', '3777fa4d-0220-4494-89e1-6fdddd8ed2d4', 'IMAGE', 'https://cdn.chotot.com/pv8KbA784zE_dWpw8ez1KBNVW7MWOwhUy8od937BwpU/preset:view/plain/69d6173983b17ecfa8246f4dcb8e6e5b-2996121881760548324.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3cb2b785-a216-4c0c-8713-603b44233cde', '3777fa4d-0220-4494-89e1-6fdddd8ed2d4', 'IMAGE', 'https://cdn.chotot.com/nVcqorqGUVzFRlM7aaQl2eshR15ysN6sy93Log290u0/preset:view/plain/8b852912fcbbb9533b265c937cd25289-2996121881737074841.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e49dba39-eb00-47e5-a7fe-59b28a8ed930', '3777fa4d-0220-4494-89e1-6fdddd8ed2d4', 'IMAGE', 'https://cdn.chotot.com/Wmx_6hXZ1oNVANpW872zyTcSH3zSbvEnVt0EHAPT-4o/preset:view/plain/a06c68a08d3d2c104c2d5fc2db799556-2996121881864398502.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4be939a1-5f91-47ab-a59c-b2fc312d351c', '3777fa4d-0220-4494-89e1-6fdddd8ed2d4', 'IMAGE', 'https://cdn.chotot.com/JrOS3YHM0noHek-3jIqEVij_ECeHoBhQcIN96jWM4sQ/preset:view/plain/421af7d70eeb002e4fd88ba3a0a41ecf-2996121881869295704.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9c658a39-ffab-4c83-853c-c1ba7ef71e2a', '3777fa4d-0220-4494-89e1-6fdddd8ed2d4', 'IMAGE', 'https://cdn.chotot.com/r0x7hajZDzznS1AAVNV-C8y5XpRQZ7ihZOt5QPd8wfE/preset:view/plain/c2a963545a4c25947f7e7fd44952857b-2996121882248795135.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ce60fd1e-ac74-4f9d-9668-03e8a7707c04', '3777fa4d-0220-4494-89e1-6fdddd8ed2d4', 'IMAGE', 'https://cdn.chotot.com/t57rHmeLmMWqx-N4_QVLml_DiYJj19FMvYnO3L0RqKo/preset:view/plain/f644e6be6a58a99b1ebc58dbb6e7ed1c-2996121882135419799.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('ed81525e-8df5-48f3-91c2-74189a5c2c01', 'P_131859461', 'APARTMENT', 'Căn hộ studio mới thiết kế hiện đại Full nội thất gần Lotte Q7', 'Dự án: 
Thông tin chi tiết: Căn hộ mới xây
Vị trí Đào Sư Tích 
Nội thất : Kệ bếp trên dưới, tủ quần áo, tủ lạnh máy lạnh máy nóng lạnh bàn ghế 
Cọc 1 tháng
Gia 4tr9
Nhà mới đang set up nội thất 
liên hệ xem thực tế ngay nha', 'UNDER_OFFER', 'Huyện Nhà Bè, Tp Hồ Chí Minh', 30, 4900000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('aae935a6-89d2-486f-b022-b7b30cfb7603', 'ed81525e-8df5-48f3-91c2-74189a5c2c01', 'IMAGE', 'https://cdn.chotot.com/xuWOgsMWoGPIHTO6BJ65DF4H-hPsFiFVho6m1G9EpbY/preset:view/plain/65913c6e771d5af928eebb700e6adffd-2994386627800183229.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d8b4a253-5d88-407b-bd2f-70b9d80ee24d', 'ed81525e-8df5-48f3-91c2-74189a5c2c01', 'IMAGE', 'https://cdn.chotot.com/jc5olD-LIqY8REHmgWL9t-RW8C5F3pvzN5mlku-fJWU/preset:view/plain/aa672cec1dff1f718d2310e82b845ec9-2994386628679243692.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('85964af0-f91c-4156-b4e0-719e5cb383f7', 'ed81525e-8df5-48f3-91c2-74189a5c2c01', 'IMAGE', 'https://cdn.chotot.com/RywnQ8_LNt5kdK-__MH_FvQCPsYQeaF7N39Mk_mH1Bs/preset:view/plain/cce69c46530fdc5ed70fc126f8350d3f-2994386628644956417.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('38073347-7551-4f5d-9019-9fcb9bcb7c67', 'ed81525e-8df5-48f3-91c2-74189a5c2c01', 'IMAGE', 'https://cdn.chotot.com/fNdCpli8q5pXHjxOSjw2WIKLc6kQSc0WBpPexwXmVc8/preset:view/plain/76209940ef79307f855e3a8bd59e2ee6-2994386629058539965.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('71a8e69a-9761-4d4a-bf32-8123011e3af8', 'ed81525e-8df5-48f3-91c2-74189a5c2c01', 'IMAGE', 'https://cdn.chotot.com/7EBYYa0Z6R88MSog2_XRfwQz0kAntN8hHHSy6tBxQUU/preset:view/plain/17c6abdd22866d1a905e7c76bfd30cc4-2994386628867695185.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('41e33d63-12bb-47ee-acb9-451be32b87fb', 'ed81525e-8df5-48f3-91c2-74189a5c2c01', 'IMAGE', 'https://cdn.chotot.com/q0fr2umjVqPAblc96rRo7EeNiwOEdYRyklOeuLWyY8s/preset:view/plain/032af9df898655576c06d3c7ece191af-2994386628695096182.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('b992858f-27ce-44d8-96c1-4762e3aac7c0', 'P_103931863', 'APARTMENT', 'CHUYÊN CHO THUÊ CĂN HỘ SUNRISE CITYVIEW LH :', 'Chuyên cho thuê căn hộ cao cấp
Sunrise City View Quận 7.
* Studio: Full nội thất đẹp giá 12tr - 13tr/ tháng.
* 1PN, 1WC: Full nội thất đẹp 13tr - 14tr5/tháng.
* 2PN, 2WC: Full nội thất đẹp 18tr - 20tr/ tháng.
* 3PN, 2WC: Full nội thất đẹp 22 - 25tr/ tháng.
Liên hệ xem và trao đổi trực tiếp Minh Anh.', 'SOLD', 'Quận 7, Tp Hồ Chí Minh', 48, 12000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('49312270-f917-4d09-a246-f2f5125f6933', 'b992858f-27ce-44d8-96c1-4762e3aac7c0', 'IMAGE', 'https://cdn.chotot.com/5rp2afhIFOmjIP0VrqtbJvYmyuPAF4r_0XfRmRzYHPw/preset:view/plain/d954f5ce603ce136020f5083a3156a37-2823893912106743275.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2f17f023-2615-4af9-9f91-15e4efba3c20', 'b992858f-27ce-44d8-96c1-4762e3aac7c0', 'IMAGE', 'https://cdn.chotot.com/eqwQOTaZs3L8g4bTkfaBI94NBla4Nh0Xs7rTKZZli3M/preset:view/plain/eaf6abaa66517f842344b3e9d74d8e2e-2823893912111885388.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ce332f6e-c35b-450a-b52e-81bc477bcf2e', 'b992858f-27ce-44d8-96c1-4762e3aac7c0', 'IMAGE', 'https://cdn.chotot.com/nFBA63Fx-AA5pSRw55_33LDoZe3wSwq-lI_rznms-TY/preset:view/plain/f711f95dfc7467eca3df7a21f486d591-2823893912100715251.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('168442ee-3502-4d81-a2e1-2a48dd325fed', 'b992858f-27ce-44d8-96c1-4762e3aac7c0', 'IMAGE', 'https://cdn.chotot.com/pDPy9cB9d5O4yMfmtqbElnFeqeo4n2FR7nNoY93tIjs/preset:view/plain/d21d76f60ab3033adb6f3867b0d6e040-2823893912198966542.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('99bb1473-fcd3-41e6-a5f6-a9b595841805', 'P_104210865', 'APARTMENT', 'Cho thuê Officetel Sunrise CityView Q7 lh :', 'Cần cho thuê Officetel Sunrise CityView Q7,diện tích 39m2 giá thuê 11tr/tháng.Liên hệ xem trực tiếp Minh Anh.', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 39, 11000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e1b11311-bc3e-453f-8b96-474b9dd3d873', '99bb1473-fcd3-41e6-a5f6-a9b595841805', 'IMAGE', 'https://cdn.chotot.com/fjVmQMXa6PUL2mD93SfqyiV8XgGeGe-cU0QM7Fp8Ack/preset:view/plain/1a6cfab4185bcb3f65ea17c5a4758e62-2815481036441075195.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e496e390-bf4e-4246-af9f-54930b05a9e6', '99bb1473-fcd3-41e6-a5f6-a9b595841805', 'IMAGE', 'https://cdn.chotot.com/7JyNOuXi18fcSVcLH9L21HXc3aYdV8nEvWuosPwaS40/preset:view/plain/c82ebab568163edec653b9f76e627134-2815481036481747173.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0c61df40-962b-47d5-a31b-152b2efaf7db', '99bb1473-fcd3-41e6-a5f6-a9b595841805', 'IMAGE', 'https://cdn.chotot.com/2DX4LlesJ6aU65erBSg2Yfu3zkJIe-svHz0TNaiGXNk/preset:view/plain/e4273ced9f62bdbab55b67e93b289f78-2815481036521889331.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('401df6fe-3856-4a90-b6d7-1ca0c7517795', 'P_133616987', 'APARTMENT', 'Bán căn hộ Cityland Park Hills 2pn 2wc full đẹp sổ hồng chỉ từ 5,1 tỷ', ' BÁN CĂN HỘ CITYLAND PARK HILLS – BLOCK MỚI – SỔ HỒNG LÂU DÀI
Căn hộ 2PN – 2WC rộng rãi, full nội thất đẹp, chỉ cần xách vali vào ở.
💰 Giá bán chỉ từ 5,1 tỷ – Mức giá cực tốt cho căn block mới!
✅ Sổ hồng lâu dài, pháp lý rõ ràng.
✅ Thiết kế thoáng mát, không gian sống tiện nghi.
✅ Khu dân cư cao cấp, an ninh 24/7.
✅ Đầy đủ tiện ích: hồ bơi, gym, công viên, siêu thị, trường học, khu vui chơi...
📞 Liên hệ ngay để xem nhà thực tế và thương lượng trực tiếp với chủ. Căn đẹp – giá tốt – chốt nhanh kẻo lỡ', 'AVAILABLE', 'Quận Gò Vấp, Tp Hồ Chí Minh', 73, 5100000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3aaf908d-79bf-4ebc-8fb4-d405c68d6ed1', '401df6fe-3856-4a90-b6d7-1ca0c7517795', 'IMAGE', 'https://cdn.chotot.com/tsItcqZtJ1Cy0tvM_6NCbpl68Xgrh5d1au-llCqEDiA/preset:view/plain/b288497ef5c1d8a4d722da03d752aa04-2994394785502198646.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5ba3202d-d18d-4965-b954-75a42350bcf9', '401df6fe-3856-4a90-b6d7-1ca0c7517795', 'IMAGE', 'https://cdn.chotot.com/DoSQW6ls-AGCovIPbpkaecKz-cVOe7jpZhj_Gd-U8QI/preset:view/plain/5a66adc861583677312150e6f62a4482-2994394783697608853.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a0638894-c763-4807-b00e-40cab2f4febe', '401df6fe-3856-4a90-b6d7-1ca0c7517795', 'IMAGE', 'https://cdn.chotot.com/Y8Jyu4bw0AVnqRtWe3Jy0RZ0Z05ZSqF0fXGhqvueoXQ/preset:view/plain/48f32c7160d80b5ef9a7f1fcc687c8d7-2994394786843207620.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0f562b27-20ef-4aa4-aa36-b27e4d82dc26', '401df6fe-3856-4a90-b6d7-1ca0c7517795', 'IMAGE', 'https://cdn.chotot.com/3y-3dPpmf_rtdiS6Br4mxW9Dwp3WCVhhKfrJhtH8T5g/preset:view/plain/37d4097ee30b8e09a5e5bfcf88d4e974-2994394788412137621.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('08db53cd-5827-47f0-b065-9b7e250c6d8c', '401df6fe-3856-4a90-b6d7-1ca0c7517795', 'IMAGE', 'https://cdn.chotot.com/RoLCjzlFrKSaqEk7G2U4Y4DZaEAdKzTzVna8Oi8yl8A/preset:view/plain/1faaa6bf7e69ce5a5f60361cd9f52893-2994394801960844150.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('085e6158-af36-45b2-bd8c-9d5fd3535a85', 'P_133940657', 'APARTMENT', 'KHAI TRƯƠNG CĂN HỘ DUPLEX CỬA SỔ THOÁNG MÁT SẴN NỘI THẤT CƠ BẢN', 'Dự án: 
Thông tin chi tiết: 📍Địa Chỉ: Luỹ Bán Bích -  Tân Phú

       GẦN ĐẠI HỌC VĂN HIẾN VÀ CÔNG THƯƠNG

Tiện ích: 

- Giờ giấc tự do
- Gần chợ khu tiện ích
- Bạn bè đến chơi thoải mái
- Gần Đầm Sen
- Mặt tiền đường lớn
- Thuận tiện di chuyển quận Trung tâm

☎️Call,Zalo: l Tri', 'AVAILABLE', 'Quận Tân Phú, Tp Hồ Chí Minh', 30, 4300000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e4292746-baec-4402-b79a-84e21e553188', '085e6158-af36-45b2-bd8c-9d5fd3535a85', 'IMAGE', 'https://cdn.chotot.com/WQrF3IHpXd4TzKTzgcf4j3msjfjOaEFmmCfwK5ctTQA/preset:view/plain/2a19d763040ca8df369e016caa6779c0-2996122028278859236.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e6942892-c0e0-4663-baae-d014d44bf120', '085e6158-af36-45b2-bd8c-9d5fd3535a85', 'IMAGE', 'https://cdn.chotot.com/OkscLU36MiqTTD-X8qhIWmsaHAA_T7zsjmB5Tx7O2Nk/preset:view/plain/36b4fc12f56b43bda507ff8816a794e5-2996122028466756503.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c6d5b838-5001-406e-8b12-83f0700b7c6a', '085e6158-af36-45b2-bd8c-9d5fd3535a85', 'IMAGE', 'https://cdn.chotot.com/sV2YlhuTy7Zj3xecj1qCPs1njyayDXcPIVjWbAXx3CE/preset:view/plain/de184cdfd16dfa6c9c83d5f5eb33350b-2996122028418932824.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('48edae8b-f0e5-44ab-8d69-c170e9d6bd1d', '085e6158-af36-45b2-bd8c-9d5fd3535a85', 'IMAGE', 'https://cdn.chotot.com/88UUsBqpkjDVG9xqzJzt7FLd53mvT62VQxzb_rK8oSg/preset:view/plain/89d8984c21d0615a5c1a619cbb60a88f-2996122028489259757.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ec47cae1-dd31-41f4-8ad7-3e898ea88966', '085e6158-af36-45b2-bd8c-9d5fd3535a85', 'IMAGE', 'https://cdn.chotot.com/IWEOlQdbaNhzVtxbH8aLAX4zmEDs6I8SABD6oHwD-l8/preset:view/plain/0403d90f549abdeedbec454bb6015ea1-2996122028548122278.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c0c1180e-2ef8-4df4-9f7f-9cb244187f37', '085e6158-af36-45b2-bd8c-9d5fd3535a85', 'IMAGE', 'https://cdn.chotot.com/6CBdGFmAMW8x72AScsNtVc1M-zhlhEapsxUmxO_AvdE/preset:view/plain/756b350be25c8d497def0d45ac9fa2da-2996122028565364237.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d2858486-0a86-4666-8dac-5051bd813f4e', '085e6158-af36-45b2-bd8c-9d5fd3535a85', 'IMAGE', 'https://cdn.chotot.com/tfN40cg4jonMzmipshw5V7pHV97Jvfv1L8542PyMKuo/preset:view/plain/227f301d4d64ee7eb1a0d9d1489e76bc-2996122028526225819.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bb59865a-2375-4289-89ac-47736f2e7591', '085e6158-af36-45b2-bd8c-9d5fd3535a85', 'IMAGE', 'https://cdn.chotot.com/7KT6K63lZJ6_71CzjaL2hWyoFSlCcP8N5Rnh1kqaJyM/preset:view/plain/c7f6f5d18c555fbf3ed8fd00a82baa62-2996122028435678244.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('438bbc74-170a-415d-aa7d-21c03d3d9d82', '085e6158-af36-45b2-bd8c-9d5fd3535a85', 'IMAGE', 'https://cdn.chotot.com/q0YkaHahumZ_MoMRyQ3ev9RJsG-BGE0Mx2PGBMnHa0A/preset:view/plain/dbb94d5ace475a331ac4c7c55e9a6bdf-2996122028517725480.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8bd74072-a1c4-42a9-98f9-5e93b577b685', '085e6158-af36-45b2-bd8c-9d5fd3535a85', 'IMAGE', 'https://cdn.chotot.com/f-9q5P6vRiOxQbJxC8LFroQ-Kp-KCjvHVO279eNFvA8/preset:view/plain/e30b0e35209b3f449f4f9e0dc62811e6-2996122028529931263.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8574611b-0a42-4a41-bcbf-e59aaba1ae43', '085e6158-af36-45b2-bd8c-9d5fd3535a85', 'IMAGE', 'https://cdn.chotot.com/-xcLo--v9UxPOtIuX1vgqmyl6bH6tz7X3rYc3jfilw4/preset:view/plain/ca964792d4396613b799e1aa0f99089f-2996122028583917649.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('b74b4e0a-9b8f-419f-a9ff-35e1644589c0', 'P_133940645', 'APARTMENT', 'Cửa Sổ Trời Gần Global City - Đỗ Xuân Hợp Full Nội Thất', 'Dự án: 
Thông tin chi tiết: Cửa Sổ Trời Gần Global City - Đỗ Xuân Hợp Full Nội Thất

- Ra vào vân tay, giờ giấc tự do
- Có sẵn nội thất: Máy lạnh, tủ lạnh, tủ quần áo,…
- Cho nuôi pet
- Có máy giặt chung', 'AVAILABLE', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 30, 4500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('690dae21-d1f8-4c1b-8cb2-bfc09d7e3383', 'b74b4e0a-9b8f-419f-a9ff-35e1644589c0', 'IMAGE', 'https://cdn.chotot.com/VadCts_gt2xJlclujRZeFSskqmsLf56bePem0oex-KQ/preset:view/plain/4e6ec5c8b4e15de5db66bcab867b017d-2996121722794001892.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bd0e2799-4f5b-40a5-a08e-0890cc93361c', 'b74b4e0a-9b8f-419f-a9ff-35e1644589c0', 'IMAGE', 'https://cdn.chotot.com/EXH_jGC33WOSP1gbe8HkoBCDf_UYfHGrDoYiz5NK55s/preset:view/plain/9e7dcb33449d2272b5308ed7e079bb37-2996121731056310353.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2a3da3d0-93ca-4107-a2b1-145732ea7d33', 'b74b4e0a-9b8f-419f-a9ff-35e1644589c0', 'IMAGE', 'https://cdn.chotot.com/zYghKMhWEYuQMI-CVb9wKWJv5Ij42Ttivp7cXQZnBIE/preset:view/plain/1ca7be34746a73ecd93f90fe3a1babd8-2996121731101019844.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('83c1992d-e313-41f1-add4-b924252be778', 'b74b4e0a-9b8f-419f-a9ff-35e1644589c0', 'IMAGE', 'https://cdn.chotot.com/IpnLRN7VcGa2zjHrExrn81TI57TVx5qt_jqLr3EKSoo/preset:view/plain/170f220cba240eced1827493d3474b39-2996121731137693350.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ea65604a-33f9-40c0-9751-9a31b7dcb052', 'b74b4e0a-9b8f-419f-a9ff-35e1644589c0', 'IMAGE', 'https://cdn.chotot.com/-_teF3-BHYiDp1nm4umEunOtNvstiQsx3Im3ThyTEEo/preset:view/plain/31ae1c3b5eebf7d4f492a5b6c3166a07-2996121731171778061.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('44f99ff6-362e-463f-8478-8f31e05b6f7b', 'b74b4e0a-9b8f-419f-a9ff-35e1644589c0', 'IMAGE', 'https://cdn.chotot.com/ZrExjrLD3OTy4xhx8ZawuGLkCgqXyyYvXPy0UO_w310/preset:view/plain/72c4add872a3f380f373ae00a5b30d59-2996121731202654952.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6fb7982a-8e17-4931-b8d9-ee7de0fdc856', 'b74b4e0a-9b8f-419f-a9ff-35e1644589c0', 'IMAGE', 'https://cdn.chotot.com/pZDplXrJVRm8EyCRLkkmO1CSUgKysWYVC6RMeQyuHXs/preset:view/plain/6dc86bb1475260d2fcbcee2b32f94a35-2996121731233714406.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9a30319f-eb33-4112-be4e-a299920e26b3', 'b74b4e0a-9b8f-419f-a9ff-35e1644589c0', 'IMAGE', 'https://cdn.chotot.com/mW3rDbX25qKUqs6evSGt3djjLO1gXRwbl8ILipOiUr8/preset:view/plain/dac7cd5e9718ea9f1c0f2b62a3cb3ede-2996121731619471118.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('14f45ee0-1166-4e63-8490-78db3792551d', 'b74b4e0a-9b8f-419f-a9ff-35e1644589c0', 'IMAGE', 'https://cdn.chotot.com/0nONq1y-zp1Pd7OZUJgXVXGKxoNRkMgY4O5OM5l0H18/preset:view/plain/6939152166835fd3ade3ce6ba1a5fa4a-2996121731276546136.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e66240fe-2e83-4241-a881-d4e77eecd292', 'b74b4e0a-9b8f-419f-a9ff-35e1644589c0', 'IMAGE', 'https://cdn.chotot.com/9yxhbZJiYreQNTxv-9ZVk7Qd2BXhoPqH3HGoVzm2NUc/preset:view/plain/4124aee875b6a393b2712ce1fb143bbd-2996121731297196781.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('ec877c2e-ec13-4e1e-af20-9177a746f831', 'P_129763614', 'APARTMENT', 'Sàn giao dịch CĐT - Phúc Yên 1/ 122m2 - 3PN 2WC - 5.28 Tỷ - Lầu thấp', 'Chung cư Phúc Yên 1 tọa lạc tại 33 Phan Huy Ích, Phường Tân Sơn, TPHCM.

- Căn hộ có diện tích 122m, thiết kế thông minh, mang lại không gian sống thoải mái.
- Gồm 3 phòng ngủ và 2 phòng tắm, phù hợp cho gia đình nhỏ.
- Pháp lý đầy đủ, đảm bảo an toàn cho giao dịch.
- Giá: 5,28 tỷ.
- Sổ hồng riêng.

Địa điểm xung quanh:
- Gần bệnh viện đa khoa tâm trí Sài Gòn.
- Siêu thị Winmart + và Bách hóa xanh chỉ trong vài phút di chuyển.
- Các công viên như Nguyễn Sỹ Sách và Cây Sộp, lý tưởng cho việc thư giãn cuối tuần.
- Trường tiểu học Lý Tự Trọng và trường mầm non Anh Đào Quận 12 gần kề.', 'SOLD', 'Quận Tân Bình, Tp Hồ Chí Minh', 122, 5280000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1eca57d2-e920-4232-b9b7-34dae8a73389', 'ec877c2e-ec13-4e1e-af20-9177a746f831', 'IMAGE', 'https://cdn.chotot.com/T2rqqDnE5tg-tH1TQiI3lDw9u9_sH0Q59oW1HdHzFd4/preset:view/plain/70bd97130596cfbe2411348ff2f95f5d-2987252108914016957.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('19ed88f7-4e84-4615-b119-f8a8b45d24fa', 'ec877c2e-ec13-4e1e-af20-9177a746f831', 'IMAGE', 'https://cdn.chotot.com/vzfyRmWIXIVwSA6l-y44qQVHIS5vWn7O4Ff8h8_c6Mc/preset:view/plain/53fb08ee4d0e89c2df17ad5a35716586-2987252108981430991.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2bd06834-5cf0-45d4-ae00-48f6ba13ea1c', 'ec877c2e-ec13-4e1e-af20-9177a746f831', 'IMAGE', 'https://cdn.chotot.com/GtsQiQndS2G2esDAS6f8DRBAEls_zUMx3KaQkw6IiqI/preset:view/plain/cd286974fb498999783751f302fc1289-2987252109107559999.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0740b45d-03e5-491f-b8c9-26e381fce612', 'ec877c2e-ec13-4e1e-af20-9177a746f831', 'IMAGE', 'https://cdn.chotot.com/SFi_qtHD3XtOGLRN9U8q-E80fZVWvFa3XlwNidXTn6w/preset:view/plain/b8be6050e52fec72f9ac4121cb23b1ec-2987252107891716334.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7efeca9f-9f75-4e4e-8ebb-fc7094f22cdd', 'ec877c2e-ec13-4e1e-af20-9177a746f831', 'IMAGE', 'https://cdn.chotot.com/hdmgcusuQSzupLj8aHOFW6Zfv8zwXEBMxwOfdTWXW7g/preset:view/plain/8ed662a794f36c05538b90d8ed1e65aa-2987252107978589058.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ae69fe1c-f46a-4d98-9acd-ad59f022303f', 'ec877c2e-ec13-4e1e-af20-9177a746f831', 'IMAGE', 'https://cdn.chotot.com/wxoGQBqNpaqz_1v0-fmsa_XBTK468NDz_o7MlOX4jFo/preset:view/plain/145e327d819d0a510e80e4b75114e394-2987252107769646316.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0be364aa-1218-408b-b3ea-c5018431f1a2', 'ec877c2e-ec13-4e1e-af20-9177a746f831', 'IMAGE', 'https://cdn.chotot.com/F-J6soj4-VR-F1fqnob-Yv6wMUGfrksSsZkWWv01o_Q/preset:view/plain/332627e6fba096d9165de67c09e8fe2d-2987252109614206162.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('09d6ecef-8390-4b50-9a95-3cc883ceb015', 'P_132586733', 'APARTMENT', 'Phúc Yên 1- Penthouse 4PN 4WC 195m2 - 23 triệu - Đủ nội thất', 'Phúc Yên 1 - 33 Phan Huy Ích, P. 15, Tân Bình. 
DT: 232m² 4PN 3WC.
Giá: 22 triệu.
Cọc: 2 tháng.
PQL: 7.000/m².
Điện nước theo nhà nước.', 'SOLD', 'Quận Tân Bình, Tp Hồ Chí Minh', 232, 23000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ce83fa75-e928-4083-9fc1-b933d8885ad7', '09d6ecef-8390-4b50-9a95-3cc883ceb015', 'IMAGE', 'https://cdn.chotot.com/94b5Yd_qWsZp22-n4O2D8Y6wO8q67NvG8hANEKoulh0/preset:view/plain/9388138d10e782af52077ba1bac92e88-2985802841096943700.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('02a13ca9-5d6b-400a-a796-e90fc3691bfd', '09d6ecef-8390-4b50-9a95-3cc883ceb015', 'IMAGE', 'https://cdn.chotot.com/nYp0HYoWIv0mXYR9UlOYrmD39bdRYmLMx97wuAHbRj4/preset:view/plain/039bc48c89014c1e2718aca1e5344aa7-2985802841383385163.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5e14bd4b-829f-47c7-9fca-5a65cf0dd7ec', '09d6ecef-8390-4b50-9a95-3cc883ceb015', 'IMAGE', 'https://cdn.chotot.com/qUfZkkbiAAL6DXJnu4Pte5QxgLLe-RJlEBLIAD1MGIE/preset:view/plain/f793b67a12240c4d061533a83a2277a3-2985802841327952207.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('115f07ab-1ae5-4902-beaf-2235b9f5131f', '09d6ecef-8390-4b50-9a95-3cc883ceb015', 'IMAGE', 'https://cdn.chotot.com/AZukhe_NAQWytUQyh4EAoZ2EWFPfNGJ5ULIt_wWUhTA/preset:view/plain/95b4519aedd1ac81b53e039b7916bf5e-2985802841987300553.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('710c9510-2cd0-41ae-8935-f12e3ac86345', '09d6ecef-8390-4b50-9a95-3cc883ceb015', 'IMAGE', 'https://cdn.chotot.com/qGHsgmxgzPyVlisKMLRCs7etoX_haY1qR-e56y1Rdeo/preset:view/plain/c0b2257ed22676523a8f8ffa6cbc9299-2985802841127349081.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('154633f5-0b45-4f97-9493-02abd953c45d', '09d6ecef-8390-4b50-9a95-3cc883ceb015', 'IMAGE', 'https://cdn.chotot.com/1sDwiEbiz2j_1FkullMkGCtomxgpAdAK7jU3GU56D3E/preset:view/plain/c6431f21d71bc2bb34bca454e95ec0ef-2985802840936938011.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('1614a637-b835-44a6-ae37-da8438a38196', 'P_133940637', 'APARTMENT', 'Cho thuê Studio - Hùng Vương,  Có ban công, Có cửa sổ', '🏠 Studio -  xxx/xxx Hùng Vương, Phường 9, Quận 5 (Phường An Đông), Thành phố Hồ Chí Minh
 📐 34m²
✨ Có ban công
✨ Có cửa sổ
----------------
_PHỤ PHÍ:
- Điện: 4.000
- Nước: 150.000
- Gửi xe: Miễn phí 2 xe
- Dịch vụ: 200.000
- Phí khác: • Ở người thứ 3 thêm phí 100.000đ', 'SOLD', 'Quận 5, Tp Hồ Chí Minh', 34, 11500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fa22763a-68f3-4d9a-9fea-74c5ad9637b3', '1614a637-b835-44a6-ae37-da8438a38196', 'IMAGE', 'https://cdn.chotot.com/BnNZRoCPohoWrPccy18Yt5PzwG2g_8hk5XoS8691-8o/preset:view/plain/32d45c4f3d2f826707a47a4646730abc-2996121550584322201.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9840eb03-a679-420c-a1bc-1ffe5bafb2e7', '1614a637-b835-44a6-ae37-da8438a38196', 'IMAGE', 'https://cdn.chotot.com/0EmsodYiw2A1KNMaBYNWX4iujTR1aYhBTNyeO5yeW-Q/preset:view/plain/58d74825e7c3a68f576c7d625fb75148-2996121550511753593.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('95cb44dd-fb87-4be3-bb87-940712800446', '1614a637-b835-44a6-ae37-da8438a38196', 'IMAGE', 'https://cdn.chotot.com/4dCLpZ7v8AI8ryxiBUOlNPMqrK2Kw6j8sZxu2HM2XWI/preset:view/plain/cf7fbf44ce9b5f808a6860a9a73a1597-2996121550734351255.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ab01afc5-54f2-4773-8410-e313fc6e5f32', '1614a637-b835-44a6-ae37-da8438a38196', 'IMAGE', 'https://cdn.chotot.com/-XVfeJ9cl0Kqw6h93ksI4H9uqNGwQ6rik0QKNNMgk40/preset:view/plain/c6ea6a06e49002fb2460f0a704fb0c63-2996121550621194989.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('191ad4b0-62c1-417d-bb1b-c32967c725f8', '1614a637-b835-44a6-ae37-da8438a38196', 'IMAGE', 'https://cdn.chotot.com/ystYOm0jBKNZJED4Jv3D4KahWObhdxqfS3eeUgiZjsU/preset:view/plain/2a90df5e7f44ad89a1d75757b2b43627-2996121550717668967.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d14c4403-cafb-44c9-bea4-557c4d52c7f5', '1614a637-b835-44a6-ae37-da8438a38196', 'IMAGE', 'https://cdn.chotot.com/ixXW7b-UcaObCdjjjArK4WzvyymXbowNE8qRjd90-mk/preset:view/plain/ec76fa65ddfb549da959abf642aca004-2996121550696650024.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0065d56e-06c2-4292-8a3d-7d78bb90e62c', '1614a637-b835-44a6-ae37-da8438a38196', 'IMAGE', 'https://cdn.chotot.com/tmNmriWPthxEGhcKwEK77YcNi_xMYT1USFTm9AP3mz4/preset:view/plain/f0a825d04a33c3117adf0ddf3a32b560-2996121550712022486.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9563d35f-cc94-43af-ac4b-518fa18fd5d3', '1614a637-b835-44a6-ae37-da8438a38196', 'IMAGE', 'https://cdn.chotot.com/0k8xiJZKcCYFM_fLIYN7i2gtdnJaZZcV5iVG5Pmf80I/preset:view/plain/81ef2d8ae5ce61491b05cff4d22b5ca8-2996121550701928536.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('a88c2839-4e02-4c4e-9b51-2a5e25e3e596', 'P_133940632', 'APARTMENT', 'CĂN HỘ 2PN', 'Dự án: 
Thông tin chi tiết: 2 phòng ngủ. 2 nhà wc
3k8/kw
Nước 100k/ người 
Dịch vụ 200
2 pn 
Ban công rộng 
Full nội thất như hình', 'UNDER_OFFER', 'Quận Gò Vấp, Tp Hồ Chí Minh', 30, 6300000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('76c5381d-af33-4ce2-9605-4fcb5e29c179', 'a88c2839-4e02-4c4e-9b51-2a5e25e3e596', 'IMAGE', 'https://cdn.chotot.com/P3Slql3Dy4tnbJ5m3g829XdkfLwEKVj4klpBGDJG2WM/preset:view/plain/765e8843c4640a4a825c41fb33874f9f-2996121902977226905.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a9487edf-0fc7-4cad-9231-ea54be627f53', 'a88c2839-4e02-4c4e-9b51-2a5e25e3e596', 'IMAGE', 'https://cdn.chotot.com/M5EkGKab4ZO88X_6DHzXBB5oBDGLFYvnnhw0ZAH4Lz0/preset:view/plain/01a943349675be91aee7ad4a14ee89ae-2996121903142936664.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('35fae147-07c7-4d8b-9542-5a4a858fee5e', 'a88c2839-4e02-4c4e-9b51-2a5e25e3e596', 'IMAGE', 'https://cdn.chotot.com/kNX3bCay0SMKYEVFRq7bBX6YfcyTVOnhV_P3p99JU_Q/preset:view/plain/77b4be7acc5ec3c39684a068a3fe8486-2996121903384840603.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ef4f2262-921e-4e75-92a6-049eb43e3785', 'a88c2839-4e02-4c4e-9b51-2a5e25e3e596', 'IMAGE', 'https://cdn.chotot.com/P6kWYYCtntsFraW72pPN-3jv8jCsvWtSfPm9qw-vgtI/preset:view/plain/e3ecd9673c19bd9fd7dcd453101a24b0-2996121903358729111.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('606ec2ab-6c52-41bf-a241-316b933d7ff3', 'a88c2839-4e02-4c4e-9b51-2a5e25e3e596', 'IMAGE', 'https://cdn.chotot.com/z6EKvKMY896mkv-urSL69buWp0fQM-JpikdWA5xVOL4/preset:view/plain/dbced21af60897141361a4867a0e6cb4-2996121903643793489.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0f35359e-6e1b-4549-9e68-79d0a8453c37', 'a88c2839-4e02-4c4e-9b51-2a5e25e3e596', 'IMAGE', 'https://cdn.chotot.com/Xni4xZGxs6k8zrWa4OCAOBbPEf6gFJ_ynLKVEEmkG4s/preset:view/plain/009a09eddf614c266bd3dd343452c7dc-2996121903356077734.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a5dae40f-891e-49aa-8ed6-c97208b8198c', 'a88c2839-4e02-4c4e-9b51-2a5e25e3e596', 'IMAGE', 'https://cdn.chotot.com/Bf_yERwq5lC2nrUlGdEyTCra7umnDj2h0-sQoCl_tso/preset:view/plain/6034cfe35acd493944636bc64ec9805d-2996121903385349173.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9ce83cf2-ba8a-4a02-ac94-98d02acb0e8c', 'a88c2839-4e02-4c4e-9b51-2a5e25e3e596', 'IMAGE', 'https://cdn.chotot.com/7buvykGAh-tJ52v4S2V2Cf41OStEZVKZZ-R6TgRw4mw/preset:view/plain/0216f75b9e63cac8df87075c5c047618-2996121903644513576.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9a3fbc2a-4690-473d-a038-e316f71236a9', 'a88c2839-4e02-4c4e-9b51-2a5e25e3e596', 'IMAGE', 'https://cdn.chotot.com/VWkrVu-ItRioMcQTannJ7uSwsaDUcdQ8SbFZ9jr7wrM/preset:view/plain/fe529e09b752d4bb719f73214cdf54e9-2996121903692217869.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f8dbfe9e-1197-4294-9842-076803d160d5', 'a88c2839-4e02-4c4e-9b51-2a5e25e3e596', 'IMAGE', 'https://cdn.chotot.com/Bqx9Uzs4f9t8c0iFJscTD-cLIIPIoQyUay4eh2nbb2M/preset:view/plain/6fa9652a30fac6a519b01db931132477-2996121903749811815.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('782e7a8d-7fcf-42a3-b469-ae9d8e94b570', 'a88c2839-4e02-4c4e-9b51-2a5e25e3e596', 'IMAGE', 'https://cdn.chotot.com/4SZ4Wztsb_zsE5ZiDXHuGAOdLdCWZ54sXUJz8ldnLWw/preset:view/plain/29548c8f5e339de616c53f51ff7d14af-2996121903595473273.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('99ac9776-8b29-4d5b-b7ad-71abb69352a1', 'P_133674733', 'APARTMENT', 'Căn cc cao cấp siêu phẩm cực đẹp chỉ 15tr 1PN 1WC tòa Botanica Premier', '💥 GIÁ TỐT – CĂN HỘ RỘNG – GẦN SÂN BAY 💥
🏙 CHO THUÊ CĂN HỘ BOTANICA PREMIER - DỰ ÁN NOVALAND  🏙
📍 108 Hồng Hà, P.2, Tân Bình – Gần Công viên Gia Định & Sân bay Tân Sơn Nhất
🏠 57m² – 1 PN – 1 WC – Nội thất đầy đủ, đẹp như hình. Check in cuối tháng 6
💰 14 triệu/tháng 
🎁 Tiện ích miễn phí: Hồ bơi, gym, BBQ, bảo vệ 24/7

📞 Zalo/Call: (Trình) – Xem nhà trực tiếp

#TheBotanica #CanHoGanSanBay #ChoThueCanHo #CanHoTanBinh #CanHoNovaland #BotanicaPremier', 'AVAILABLE', 'Quận Tân Bình, Tp Hồ Chí Minh', 57, 14000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a6995489-5f39-4c62-ac68-1853ae32f9ae', '99ac9776-8b29-4d5b-b7ad-71abb69352a1', 'IMAGE', 'https://cdn.chotot.com/3thtjX5enD2SXcQevbWXOIAXYkd-WsZX_FTwbEsxlFI/preset:view/plain/512649ba44a55c2aa3dad09d3bddf07d-2994096331330181318.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('67391d62-08ef-4057-878e-5f6cb2738f7a', '99ac9776-8b29-4d5b-b7ad-71abb69352a1', 'IMAGE', 'https://cdn.chotot.com/rA_lteGVhYXiN0A_JQvBoI5ihpG_VEGMh1YeBK7Vx5o/preset:view/plain/7617eb236e4d5d719480e3841f10a4c1-2994096331678633409.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1cfd5a79-b160-4e17-8f66-f6048e7d7855', '99ac9776-8b29-4d5b-b7ad-71abb69352a1', 'IMAGE', 'https://cdn.chotot.com/Lt8hN3vHRdHh-xA2v69g7bPuz2My-4rXFWfyhDGNFqo/preset:view/plain/d58a6ac7eaff588e3bc940b9b97ac8a2-2994096331486180542.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('beb7e048-02eb-48e4-8f94-2b913d5ec41c', '99ac9776-8b29-4d5b-b7ad-71abb69352a1', 'IMAGE', 'https://cdn.chotot.com/CAqf0WXB4lhiV325P0HY4l5hRteaPfaK3Ju3gtBkSe8/preset:view/plain/95c7f7907f6532a544a8174544c830b9-2994096331395538613.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9dd13949-67d6-433a-83b8-5b7e93ff6961', '99ac9776-8b29-4d5b-b7ad-71abb69352a1', 'IMAGE', 'https://cdn.chotot.com/mXMfVApz9O1xadqeEcrke830ppZIFFK2AhrHV4CwLFY/preset:view/plain/a67aca1591cb528bd19d33abbf97e130-2994096331806159535.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7ccdb809-dd67-4b5d-a6ab-6dfbf5932221', '99ac9776-8b29-4d5b-b7ad-71abb69352a1', 'IMAGE', 'https://cdn.chotot.com/NXFckVG51rl41gQeeayI33vlpL9LrCGDJd_BbIlAqWQ/preset:view/plain/de2798f6cdb0074818576ccb26c0f243-2994096331913810755.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2268d9e0-d526-4863-b260-3738ab226987', '99ac9776-8b29-4d5b-b7ad-71abb69352a1', 'IMAGE', 'https://cdn.chotot.com/vp8gAJUdCyeXQbIlcAriNZ_5FLF2s-U7H6l4t8mKWKQ/preset:view/plain/ce4ff1079ddb7274623644d5cb3500b2-2994096331384378501.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('48e32831-f2c8-4ccd-90da-3947174e0deb', '99ac9776-8b29-4d5b-b7ad-71abb69352a1', 'IMAGE', 'https://cdn.chotot.com/0gbWyP4aESJcGRkYxZyCPCcwYGwi8MSeI1DG7SecdSQ/preset:view/plain/057e4a283a016e25084434771e3a04aa-2994096331986724438.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('16b52cf5-91d5-4f37-b239-22198bc04e22', '99ac9776-8b29-4d5b-b7ad-71abb69352a1', 'IMAGE', 'https://cdn.chotot.com/L_2-RI9Yvp-b40xYVShVm5Vda33ruIGZJYLZoGrAcb8/preset:view/plain/9ea6b949bb2833b99572c6b8a4d54337-2994096331628329826.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('cc2d1695-b79b-4652-92c2-ccce2076aafa', 'P_133940617', 'APARTMENT', 'CHO THUÊ GẤP 2P CHUNG CƯ SUNRISE CITYVIEW VỪA Ở, LAM VĂN PHÒNG QUẬN 7', 'Chính chủ cho thuê gấp căn hộ chung cư cao cấp Sunrise cityview - 33 Nguyễn Hữu Thọ - Quận 7
Thiết kế: 2p 1wc - NTCB
Dọn vào ngay, có thể ở Hoặc làm vp

Giá thuê: 14tr/tháng - Miễn phí quản lý''
Liên hệ xem nhà 24/7: *** - Hoặc Sms - Zalo
Xin cám ơn!', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 60, 14000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4f864ad2-9d8e-4e19-b219-78ef35316480', 'cc2d1695-b79b-4652-92c2-ccce2076aafa', 'IMAGE', 'https://cdn.chotot.com/873VZRuqmWTDKTFlEKIiqRYpKT8eCeWOG5SlmNy1qA0/preset:view/plain/23fcd3f9f2ac97396ddcf0e4ca4290c8-2996121616582199673.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a3976fb7-b859-496f-ae90-ee22a566623a', 'cc2d1695-b79b-4652-92c2-ccce2076aafa', 'IMAGE', 'https://cdn.chotot.com/6o9wnUPInvhb40gxcHKUm-mVYtJ0WtJWttXgByp2NoE/preset:view/plain/a08996ad5fb8b9aa3d3c6d1c0d444e82-2996121616617350180.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('85bb1409-73ac-48df-869b-db440dabade8', 'cc2d1695-b79b-4652-92c2-ccce2076aafa', 'IMAGE', 'https://cdn.chotot.com/GvKIdxrdYoF83XflRXZiRrgAgUm_ctK55HiGfLfWw9Y/preset:view/plain/a492d676f57372d632384ce0b50a6b7e-2996121625848223897.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('815a2baf-1f2f-4a49-933a-1ee94dc33606', 'cc2d1695-b79b-4652-92c2-ccce2076aafa', 'IMAGE', 'https://cdn.chotot.com/MxFRRABXDbGHNnmOJ1c1PD5qNijoTxT3Jos1ITTCd40/preset:view/plain/be981f2fd22392c8f7ec2fc0c267be0b-2996121635096181485.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('fa70b646-a99c-42a5-af63-eebdc5e3d8d1', 'P_126451230', 'APARTMENT', '🔥SIÊU PHẨM DUPLEX BAN CÔNG LỚN FULL NỘI THẤT MÁY GIẶT RIÊNG', 'Vị Trí : Nguyễn Duy Trinh , quận 2 

- Gần Mai Chí Thọ thuận tiện di chuyển vào trung tâm
- Camera 24/24 , ra vào vân tay
- Khu vực an ninh, trang bị pccc
- Giờ giấc tự do, không chung chủ

Liên hệ ngay để xem phòng:
SĐT/Zalo:  (Thu Hiền Hifriendz)
Hỗ trợ tìm phòng trọ tại Quận 2 - Quận 9.', 'UNDER_OFFER', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 30, 5100000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('542ff97c-f9f2-42a9-a485-c69230978569', 'fa70b646-a99c-42a5-af63-eebdc5e3d8d1', 'IMAGE', 'https://cdn.chotot.com/wtpAXauN27cXVVmjFv3ySSCvm2Fn9r5T0O4Baz4rYq0/preset:view/plain/33a32bac1d78ea861d5974baae310988-2983919874482673748.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('317684aa-bfbd-41e1-a0cb-88cea5a1a775', 'fa70b646-a99c-42a5-af63-eebdc5e3d8d1', 'IMAGE', 'https://cdn.chotot.com/uCXSrKP4_FbCqaDS7dsKAYrOZaY1mJbjfG1QNxIM7EI/preset:view/plain/0dc3a0a6ec5b11da3cfe796dff8f1aec-2983919874583118727.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a861b506-59e8-42e7-a044-4ff557d441a3', 'fa70b646-a99c-42a5-af63-eebdc5e3d8d1', 'IMAGE', 'https://cdn.chotot.com/jg_rqbefZMxYCB45jfIem6EDe_CLfZ_RdQQciTm9h2M/preset:view/plain/1074d69070e88d2f200501265ac3a4cb-2983919874544715173.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ec8b62b2-fe2a-47e6-9739-ba82b205b251', 'fa70b646-a99c-42a5-af63-eebdc5e3d8d1', 'IMAGE', 'https://cdn.chotot.com/fzLIeQ07QRXvH5RUiFUlnmHzA3ANM4fZE7CRYskXZXA/preset:view/plain/3c1a8d363cf00b33e0806f8e7ca3e077-2983919874475321392.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4fe591ff-2489-4108-aafe-157fbfe5e5b4', 'fa70b646-a99c-42a5-af63-eebdc5e3d8d1', 'IMAGE', 'https://cdn.chotot.com/6qJTUiycXrq2QvTUBJxGI9R3wk-lP_b256zk1cANZVY/preset:view/plain/c0012adad923a626fda0e02ef2b3ed1e-2983919874570787338.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('5893e1f7-714e-4c4d-b28a-d6bfa6842693', 'P_133722499', 'APARTMENT', 'CĂN HỘ 2PN 70m2 NGAY CÀ PHÊ DƯỚI TÁN CÂY', 'Dự án: 
Thông tin chi tiết: 🏡353 Bình Quới, Bình Thạnh 
✅ 2PN + 1PK + 2Tolet ( 70m2) 
✅ Full nội thất
✅ Tiện ích: Thang máy, Hồ Bơi, Khu cf dưới tán cây
☎️ Call/Lh: *** (Khang)', 'AVAILABLE', 'Quận Bình Thạnh, Tp Hồ Chí Minh', 70, 11000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8bf22c19-7dc9-4100-8d79-351207c8f2fb', '5893e1f7-714e-4c4d-b28a-d6bfa6842693', 'IMAGE', 'https://cdn.chotot.com/56UTYdMdgvSBpCjZM9HPmIU6BRDJmzvchyngx025TZk/preset:view/plain/ca0026cc66709a167522ffa7949c6365-2994450658754291969.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5975ad68-7e68-44e7-905d-78b1e721fdb6', '5893e1f7-714e-4c4d-b28a-d6bfa6842693', 'IMAGE', 'https://cdn.chotot.com/yyXPHFSKc8dJC-wKLNXLmnAf2B_4poqMT4AmcdScPnE/preset:view/plain/fba810432dbfd4949e5297e56e5d8616-2994450659877245808.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f68a4a96-b5b8-48ed-87a1-cd2e574a5160', '5893e1f7-714e-4c4d-b28a-d6bfa6842693', 'IMAGE', 'https://cdn.chotot.com/Cp0iAy3lLCru6_kN4xlqD_Qa8tPlAaw1qWhqVBvJmLI/preset:view/plain/fd589d80ae2cb39f7ef9a84d5c7b3296-2994450660901841153.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('46752723-c3f4-4ef3-961d-91291e3beee5', '5893e1f7-714e-4c4d-b28a-d6bfa6842693', 'IMAGE', 'https://cdn.chotot.com/Ob1jKm7aO4yXW_MvC2e4WsLnbOQQWAjHlegb4IzGpYw/preset:view/plain/6e66c9ad67492b2c2ca5935afa66ecd1-2994450661253043056.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('2ed82b66-1e7d-435f-b4f0-a8b18ef1733f', 'P_133940602', 'APARTMENT', 'Căn hộ giá rẻ, ảnh thật ', 'CHDV MÀ CHỈ TÍNH ĐIỆN NƯỚC GIÁ CHỈ  NẰM NGAY MÃ LÒ
Thuận tiện di chuyển Tân Phú -Q6
Toà có hầm xe
Nhận thú cưng, xe điện thoải mái
Phòng siêu thoáng mát

', 'UNDER_OFFER', 'Quận Bình Tân, Tp Hồ Chí Minh', 35, 3900000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c3ee491c-9dbe-40c3-827b-3e65218b1961', '2ed82b66-1e7d-435f-b4f0-a8b18ef1733f', 'IMAGE', 'https://cdn.chotot.com/5DmFKIzbeKq32KzTrSYNBPPdkN_DLk0-rEf7rc87m98/preset:view/plain/366ee4a408fb60a1664ab94ff7a1196c-2996121784199988708.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5923523a-2f82-4e33-bc1d-96f241aaa6c3', '2ed82b66-1e7d-435f-b4f0-a8b18ef1733f', 'IMAGE', 'https://cdn.chotot.com/WQCWb3C48DAcBBMnKUM1iqP9yo9Y-aJMMX9p4ftsGZ4/preset:view/plain/a2abd0ff1d7fbbd0720e8a133fbdf110-2996121794025639527.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b2293344-49db-4133-9117-11270941b027', '2ed82b66-1e7d-435f-b4f0-a8b18ef1733f', 'IMAGE', 'https://cdn.chotot.com/TozqZGMqfqwadlspMTDIexOp6VOeGZWtE4yU-JPbiP4/preset:view/plain/a1266bee7bec7da182f9f3274cba5e19-2996121802209446265.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('cfe7fe57-80f9-4f97-a3e9-ded504e0018c', 'P_132759644', 'APARTMENT', '🌟TRỐNG SẴN DUPLEX FULL NỘI Thất - MÁY GIẶT RIÊNG - Ngay Tân Sơn Nhì', 'Dự án: 
Thông tin chi tiết: Trống sẵn - DUPLEX FULL NỘI THẤT - MÁY GIẶT RIÊNG - Ngay Tân Sơn Nhì - AEON TÂN PHÚ - Gò Dầu ,…

• Giáp Tân Quý , Chợ Tân Hương , Gần ĐH Văn Hiến , ĐH Công Thương ,….
- Phòng Trệt , Thuận tiện di chuyển 

- Full nội thất như hình - Có thể ở liền 

- Thuận tiện di chuyển các quận lân cận 

Xem phòng liên hệ : Thành Truyền để em tư vấn & hỗ trợ 24/7', 'AVAILABLE', 'Quận Tân Phú, Tp Hồ Chí Minh', 28, 5200000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c7ee40ec-4b40-4424-9914-70d2e31b72b3', 'cfe7fe57-80f9-4f97-a3e9-ded504e0018c', 'IMAGE', 'https://cdn.chotot.com/SgxHdHQtAAExLBkg7isE0nvMu7xVI4nFtqRtXJc_NXs/preset:view/plain/62c91114f931f080e148af41c6eb7237-2991340794974074274.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fdfbac26-3b9c-468d-89fd-8f012b05c507', 'cfe7fe57-80f9-4f97-a3e9-ded504e0018c', 'IMAGE', 'https://cdn.chotot.com/zU0Ujht3JAVqI15lj7VfomLOlYkyXM9Co-3--8HnVX4/preset:view/plain/8a71dda8e95f117dfdf00fee8ed253f2-2991340794988009636.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d3932b0d-786e-4885-863f-76710dff49e9', 'cfe7fe57-80f9-4f97-a3e9-ded504e0018c', 'IMAGE', 'https://cdn.chotot.com/fRMiTeK37c3m5qqtKbX7X1Zkzs5ELw3mH_w0oaKhihU/preset:view/plain/6fbe625db4deb74548e432e25b76fe73-2991340795711119737.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('86984313-e8a6-4c9c-b849-d53c81915bbb', 'cfe7fe57-80f9-4f97-a3e9-ded504e0018c', 'IMAGE', 'https://cdn.chotot.com/LyOliCax8dkceFU7MYVREDxhz54kwRmbIybvvwuSiMg/preset:view/plain/c81daf1be356c8adc31cb7a09eec6b50-2991340795638876052.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('529e679a-21b6-46b4-a877-f013a41f973d', 'cfe7fe57-80f9-4f97-a3e9-ded504e0018c', 'IMAGE', 'https://cdn.chotot.com/reilNV_x71YMUAydc1nifiWI6Hytct7DA4HCSUtzJ-g/preset:view/plain/9537ac9860b50b33f7a6275fb71f7fdc-2991340795806666137.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('927530e4-2127-4b9f-8c4d-5f7a4ddfab4f', 'cfe7fe57-80f9-4f97-a3e9-ded504e0018c', 'IMAGE', 'https://cdn.chotot.com/ThyQLqCDbfgccol0-m8nkoCyaP2ZSZQb-C04X-kwP9c/preset:view/plain/2897da7d26b2c39f1b3100323fec51ea-2991340795866532523.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('80e5937f-d9c1-4001-960a-79ee774b6d70', 'P_114804453', 'APARTMENT', '🏡 [QUẬN 2]  BAN CÔNG MỚI HIỆN ĐẠI GẦN CẦU SÀI GÒN FULL NỘi THẤT', 'TrỐng 1 PhÒNG TRUNG TÂM Quận 2
Vị trí: Trần Não 👉  Thuận tiện Ra  Xa lộ Hà Nội, Vincom Thảo Điền, cầu sài gòn.

- Nhà rộng thoáng mát. Ban CôNG LỚN
- Full nội thất, có cửa sổ thoáng.Ban Công
- Không chung chủ, giờ giấc tự do.
- Ra vào bằng vân tay, đường xe hơi tới tận nhà, quán cafe, nhà hàng, ngân hàng.....mọi thứ gói gọn trong 1km.
Lh mình tư vấn trực tiếp, nhanh chóng.
Call/ zalo: ( Chỉnh). Xem phòng ngay( Hỗ trợ Tìm Phòng Quận 2)', 'UNDER_OFFER', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 40, 8000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('edcb122f-0779-4b75-8aa8-2d2911aace4e', '80e5937f-d9c1-4001-960a-79ee774b6d70', 'IMAGE', 'https://cdn.chotot.com/l7phsn0YjmDoEkTAF6PuMiIHDscEJKMpF8_ICS_yzqE/preset:view/plain/765cc808c536374c3e4ec7153ef89306-2950590092977260897.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4f296c51-c3cc-4c70-a3e0-6d372b97424f', '80e5937f-d9c1-4001-960a-79ee774b6d70', 'IMAGE', 'https://cdn.chotot.com/Gp30KXBX2pU9rM-VKWaHC1PGwsHQMb3eIAVjYoug3Rc/preset:view/plain/2e60b87c564471251307da2aad6c0497-2950590093292778258.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b50d8301-00f9-4ce1-b813-733d3a13db43', '80e5937f-d9c1-4001-960a-79ee774b6d70', 'IMAGE', 'https://cdn.chotot.com/KO5eLmUpKpIqzoxAfjwe4ePoH9jjIXXSiwM34mkijkE/preset:view/plain/46eaff12df867ac2f5e969b6488ad372-2950590093445152667.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5ae3f1b7-85d5-4e64-aa14-c465c219f31c', '80e5937f-d9c1-4001-960a-79ee774b6d70', 'IMAGE', 'https://cdn.chotot.com/V7AJw_s06AStM_RQgsGmoR6iYT-B87vy2SUkhTvy66w/preset:view/plain/93a051cbf9ea32bea25c6022aa798e99-2950590093564824462.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('70de6023-5620-441d-94b7-d76f8e1c4251', '80e5937f-d9c1-4001-960a-79ee774b6d70', 'IMAGE', 'https://cdn.chotot.com/tS115mxIOcRZM2RMHanscuO7cksa5uNTHrYaqQoggoU/preset:view/plain/5d18e6949fb6ec1cef22d1eb22712acf-2950590093755914399.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5b29190d-a7ec-428c-8ea8-1d0f7baec385', '80e5937f-d9c1-4001-960a-79ee774b6d70', 'IMAGE', 'https://cdn.chotot.com/H2YKiQqcODUd_yg0z7cwbPufU8rVyLcH7bYStV2TNMg/preset:view/plain/e814d5846d39bb8b1eec4fdc9fbbcfee-2950590093781624187.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2697a912-e782-44fe-ac4e-771c88a222a4', '80e5937f-d9c1-4001-960a-79ee774b6d70', 'IMAGE', 'https://cdn.chotot.com/FFDc31koG5tZGq2L6J4O7xGfrmxuF2D000nyKYbK3CA/preset:view/plain/648fea6d97c4b56f7f543def5a66bfc9-2950590093881887798.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2c30bc40-1aee-4dd2-aa38-f59dbea8fb7a', '80e5937f-d9c1-4001-960a-79ee774b6d70', 'IMAGE', 'https://cdn.chotot.com/qjimLgSw_H0ZSn2LSMwF1XRtY1azJXt-HulHufSdA-Q/preset:view/plain/e644961d9519ef223537901086c6deb5-2950590093973145252.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('18312ac7-ca7c-4b3b-8193-c348393a88ce', 'P_133770520', 'APARTMENT', '1PN TÁCH BẾP NGAY KHU K300, FULL NT VỊ TRÍ SIÊU TIỆN LỢI AN NINH ', '🎊🎊KHAI TRƯƠNG CĂN HỘ NGAY KHU VỰC SÂN BAY| K300 | NGUYỄN THÁI BÌNH🎊🎊 
🏡Địa chỉ: Đường C18, P12, TÂN BÌNH🏡
😘Hiện tòa nhà có 2 dạng phòng. STUDIO - 1PN ( 20-35m2 )😘
Tiện ích:
✅ Cách Lotte Mart & Vincom Cộng Hòa 500m
✅ Cách sân bay 1,5km
✅ Tiện đi các đường Cộng Hòa, Trường Chinh, Hoàng Văn Thụ, Ngã Tư Bảy Hiền, Lê Văn Sỹ,.....
Máy giặt, máy sấy quần áo miễn phí
📲📱Liên hệ Tính (CHÍNH CHỦ): (sms/zalo/call)', 'AVAILABLE', 'Quận Tân Bình, Tp Hồ Chí Minh', 25, 6300000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c1f958fe-12a9-43c4-8e17-a4ed1dbf09ab', '18312ac7-ca7c-4b3b-8193-c348393a88ce', 'IMAGE', 'https://cdn.chotot.com/T3ybeVyYbS90UzdpAMw-vaabTusdg5u39DWpr20edec/preset:view/plain/71a9b80979c429a851cde49eec1ff842-2994829213449834481.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ba667e18-c070-4b75-94a6-45538941dd93', '18312ac7-ca7c-4b3b-8193-c348393a88ce', 'IMAGE', 'https://cdn.chotot.com/MQUCUaIX_McDp3NedQ93c-t3vjMqGC4wQvyId1ZVRIk/preset:view/plain/d1d88d59fa36fcd2f214ba111d36d37a-2994829211147757825.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e5dd6760-11e8-4075-b558-e55858a5e858', '18312ac7-ca7c-4b3b-8193-c348393a88ce', 'IMAGE', 'https://cdn.chotot.com/UjO5GdwIRZQPTer50axjMIb6EuWbvpI-1S3v9dFF2yU/preset:view/plain/2471b89908b8576cde2f165f72a61b3b-2994829212619205138.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('efb3ecf9-c6fa-495c-bca0-19e8a79ddded', '18312ac7-ca7c-4b3b-8193-c348393a88ce', 'IMAGE', 'https://cdn.chotot.com/lmar7dc-B7BV5hMEHayF-kXvJTn6fWtC6dEXeF4WNSk/preset:view/plain/f8863d06d0ade5401c4a8ee1e9a817fc-2994829212753777520.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5f0c4681-7529-48a0-b5d9-f66604b0adf2', '18312ac7-ca7c-4b3b-8193-c348393a88ce', 'IMAGE', 'https://cdn.chotot.com/DIudnY6WXIf83rntAoBn7NBk1emPg7qjkqMLE62iGro/preset:view/plain/a17b2adae258692dd9f7bf08c9c196da-2994829213123185029.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('32277a06-1fd8-48ba-83e3-52ec84627563', '18312ac7-ca7c-4b3b-8193-c348393a88ce', 'IMAGE', 'https://cdn.chotot.com/L5rNDfNrIQpQatJ0p36Z-IiMjDmHzv4NkDMlXi9QGi4/preset:view/plain/1aca8d2e64abd233130a91a9607a3902-2994829212598798721.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0042d7a1-d91b-4990-bd48-c70e85b99276', '18312ac7-ca7c-4b3b-8193-c348393a88ce', 'IMAGE', 'https://cdn.chotot.com/HXG8qKfJg7tAsoEShkZZzahJzCwWfFHvCLzyTmx_YZo/preset:view/plain/9b42fb567c52df77bf6b5ff7d5722067-2994829212529556882.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c26df48c-ce60-4077-ac40-d4d437ab83e1', '18312ac7-ca7c-4b3b-8193-c348393a88ce', 'IMAGE', 'https://cdn.chotot.com/QQ0dk7El1sq_0YpuKabAbKoMmLRTcXEhM3AVFzBnXtg/preset:view/plain/116850a520f4dae6b54d715a989d9a47-2994829212710490246.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('883297ee-a653-485a-a430-b26a39d5cedf', '18312ac7-ca7c-4b3b-8193-c348393a88ce', 'IMAGE', 'https://cdn.chotot.com/gtheY4NErqiAtYcarPC7AdO1mpI92uzzSi7zC_JD8oA/preset:view/plain/1ad76713e707c027c2ed57057acd3549-2994829213010094337.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('54ae0180-92f6-4320-805b-34f8f3abdd98', '18312ac7-ca7c-4b3b-8193-c348393a88ce', 'IMAGE', 'https://cdn.chotot.com/YpDIq1B7Q6mO0AWmnwiiHfwj3HfWaKxKV50slB-gTEs/preset:view/plain/b29c436dd28fe9c5a95ddd96b884917a-2994829213318418304.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('ff0f54d3-e7db-4c56-87cd-2d753a64bec5', 'P_133940550', 'APARTMENT', 'BÁN CĂN HỘ KINGSTON SỔ HỒNG 2PN 2WC 79M2 GIÁ CHỈ 7 TỶ ', '📣📣📣ĐẲNG CẤP KINGSTON RESIDENCE – CĂN HỘ CAO CẤP NOVALAND PHÚ NHUẬN 🔥

📍 Vị trí đắc địa – 2 mặt tiền Nguyễn Văn Trỗi & Hoàng Văn Thụ, kết nối cực kỳ thuận tiện, chỉ vài phút đến sân bay Tân Sơn Nhất. Kingston Residence cũng sở hữu hệ tiện ích nội khu cao cấp như hồ bơi, gym, BBQ, khu vui chơi…

🏡 Căn hộ 79m² – 2PN – 2WC
✨ Full nội thất đẹp, dọn vào ở ngay
📕 Sổ hồng sở hữu lâu dài
💰 Giá chỉ từ 7 tỷ – cực hấp dẫn cho căn hộ cao cấp ngay trung tâm Phú Nhuận.

⭐ Hàng đẹp – pháp lý rõ ràng – vị trí vàng – giá tốt, rất phù hợp để ở lâu dài hoặc đầu tư giữ tài sản.

📲 Quan tâm căn này inbox/zalo em để xem nhà thực tế và chốt giá tốt ạ!', 'AVAILABLE', 'Quận Phú Nhuận, Tp Hồ Chí Minh', 79, 7000000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8bfa372d-007e-4732-a0cf-dd5f2d981674', 'ff0f54d3-e7db-4c56-87cd-2d753a64bec5', 'IMAGE', 'https://cdn.chotot.com/C6z7-73jM-jsaR3T9ubTyq0XSvaLvSCPHb-aZT31xcI/preset:view/plain/43b755fa5bb0555fb085f1f2128cca51-2996121635696580761.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('022be0b6-2634-4f9a-a669-00ababf55bb3', 'ff0f54d3-e7db-4c56-87cd-2d753a64bec5', 'IMAGE', 'https://cdn.chotot.com/875A_cHcyFCenx25Zk1DwFmYhHv-5gtWSmnT_UB7CzU/preset:view/plain/c4759d325ce792f85f3ba9738d44d45d-2996121635785197028.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bb908356-e7a8-4c52-b2ab-5d985fd8e2f5', 'ff0f54d3-e7db-4c56-87cd-2d753a64bec5', 'IMAGE', 'https://cdn.chotot.com/_Qd5kkXHGjs4By_ec8H3fMMFLC8fJ-44Yf0G8rduWuk/preset:view/plain/3e5de625a5d2252bbcb2961156dcbc37-2996121636753133159.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('1eae53d4-fb4c-4429-bfb4-07b79fa505a5', 'P_118521868', 'APARTMENT', '🌇BAN CÔNG FULL NỘI THẤT🏡Gần Sala Thủ Thiêm Bason Trung Tâm Tphcm', '📌 Địa chỉ:  - Quận 2( tiện đi các quận trung tâm Q1, Q3,Bình Thạnh, Phú Nhuận,Cầu Ba Son ,…) 
 
- Phòng rộng ,Thoáng Mát
- Toà nhà có hầm xe, bảo vệ 24/24
- Ra vào bằng khoá từ vân tay
- Ban công, cửa sổ thoáng mát 
- Hệ thống PCCC, an ninh đầy đủ
- Trang bị đầy đủ nội thất như hình

☎️ Call/ZL: để được hỗ trợ nhanh nhất, tư vấn và xem phòng miễn phí', 'SOLD', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 40, 6500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8a9ecdc4-1760-4f41-a9d1-ad4caee1e7b8', '1eae53d4-fb4c-4429-bfb4-07b79fa505a5', 'IMAGE', 'https://cdn.chotot.com/33W2VLcRmIT6NVnQyKvv8U-A2zpqYaYpPdOxcDvEE9k/preset:view/plain/a6fa6edbf30e15f78f59321013ecaf20-2965301927923320821.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ab8b45fb-9940-453c-a21b-26a1ef7dc6c1', '1eae53d4-fb4c-4429-bfb4-07b79fa505a5', 'IMAGE', 'https://cdn.chotot.com/_HhaMbL2LcAX0UrtofrymW9Mg1leOBYFuLKja9NuXOg/preset:view/plain/f5ea07265f2026fa08e5134461f8d2fc-2965301928017713065.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('88467ce7-dd58-4244-9fec-f96762264ca7', '1eae53d4-fb4c-4429-bfb4-07b79fa505a5', 'IMAGE', 'https://cdn.chotot.com/WxSdhlCUrUW857ZUk1WDSbGlmt4ijBDnksPcbkATWw8/preset:view/plain/48c6452c0a397ecded1d9609aba096a3-2965301927993048597.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ae01e3cf-7630-4ddc-af85-e9439313f6f3', '1eae53d4-fb4c-4429-bfb4-07b79fa505a5', 'IMAGE', 'https://cdn.chotot.com/2NG_FsXi8akchdrDTarbpTn-W3ofO8HmRyC_fr8f8X8/preset:view/plain/0706057b084d83639b8b385a1a7ca4ed-2965301927980901632.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('88d9aa30-f64d-40c2-920e-96a7c8c8d60b', '1eae53d4-fb4c-4429-bfb4-07b79fa505a5', 'IMAGE', 'https://cdn.chotot.com/6LJtdwzPkl_soDB1IcnqqUAi8lOn0kXG3dRHkyHpO6Q/preset:view/plain/49657b9a5a022d6dbe22b847f7ac416a-2965301928101436936.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4cfac441-43ed-4163-a2c7-93d3a1b289bb', '1eae53d4-fb4c-4429-bfb4-07b79fa505a5', 'IMAGE', 'https://cdn.chotot.com/KlJIJApZ-eeCbGWDBryElN3O23ZrMXgoxRoZAvHOh_M/preset:view/plain/1c7140c958bf8d858c72577ea8e8f05f-2965301927997136437.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e0dd11ee-4ba7-452f-bf21-0b1d1966f65b', '1eae53d4-fb4c-4429-bfb4-07b79fa505a5', 'IMAGE', 'https://cdn.chotot.com/TuMQlLCaQSQ0xZoBfpe3UE8Yp_w8FbYWUCYe_s6z7xY/preset:view/plain/ef3599f99b2e724f7a0114d0d42aed66-2965301928600396565.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('ecd1a209-a9eb-4a3f-adb6-77fbcf80bad7', 'P_133940548', 'APARTMENT', 'Căn Hộ Dịch Vụ 40m2 mới 100%, Full Nội thất - Cách Mạng Tháng 8, Q3', '​✨ CĂN HỘ DỊCH VỤ 40M2 XỊN XÒ - CÁCH MẠNG THÁNG 8, QUẬN 3 ✨

​📍 Vị trí & Kết nối
​Vị trí đắc địa ngay Cách Mạng Tháng 8 (P.11, Q.3), giao thông thuận tiện.
​Gần Công viên Lê Thị Riêng (chỉ vài bước chân, không gian xanh mát).
​Gần Ga Sài Gòn, Chợ Hòa Hưng.
​Kết nối nhanh chóng sang Quận 1, Quận 10, Tân Bình, Phú Nhuận.

​🎓 Tiện ích xung quanh
​Gần siêu thị, cửa hàng tiện lợi 24/7, chợ dân sinh ngay sát bên.
​Gần Đại học Bách Khoa, Đại học HUFLIT, Đại học Kinh tế TP.HCM (UEH).
​Gần Bệnh viện Thống Nhất, Bệnh viện Chợ Rẫy, Bệnh viện Trưng Vương.
​Xung quanh sầm uất với nhiều tòa nhà văn phòng, hàng quán ăn uống, cafe tụ tập.

​🛡️ An ninh & Phòng cháy chữa cháy
​Hệ thống PCCC hiện đại, trang bị đầy đủ toàn tòa nhà.
​Có lối thoát hiểm rõ ràng, an toàn tuyệt đối.
​Có camera giám sát 24/7.
​Cửa khóa vân tay, giờ giấc tự do không chung chủ.

​☎ IB (ZALO/CALL) : *** (Feri) để được tư vấn và xem phòng miễn phí!', 'AVAILABLE', 'Quận 3, Tp Hồ Chí Minh', 45, 9000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('de5d8e2b-c870-47ca-ad19-16f15a98c8ae', 'ecd1a209-a9eb-4a3f-adb6-77fbcf80bad7', 'IMAGE', 'https://cdn.chotot.com/yAenaWdUtm0QuXAoZVFMy2_kZT5dCJT8Lcd9BWipsi0/preset:view/plain/6f3a6e7f7d727a930b42b0c4f8ed8917-2996120365303309348.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('eff69d0d-3642-4b3d-91fc-65f15394d9ee', 'ecd1a209-a9eb-4a3f-adb6-77fbcf80bad7', 'IMAGE', 'https://cdn.chotot.com/TAIadjCGMQKPDrpxAnLUWw5D8HI6KevpbEoeVUh3X-4/preset:view/plain/6c83ccb60927922e71078e21a617abcd-2996120367816021288.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2ef51907-0f11-4825-acc3-7d86096d9681', 'ecd1a209-a9eb-4a3f-adb6-77fbcf80bad7', 'IMAGE', 'https://cdn.chotot.com/5i13infJoJrCpglrCKgxEMQb4xF3wnAN9s44EyJ-_TY/preset:view/plain/ff3fd39b64d1071ee61e01c953f0f92b-2996120367981873529.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('18ec3010-529e-4849-884c-04181dd883c0', 'ecd1a209-a9eb-4a3f-adb6-77fbcf80bad7', 'IMAGE', 'https://cdn.chotot.com/DiwpZayzvlwOaBaXatNY0HeHnGgrO9n_fWduDYXFwWw/preset:view/plain/c5381df49320a0efd0cfb1c50443ef29-2996120370439797485.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4eff1b8d-6f29-48fe-8358-13fd23c6b3fe', 'ecd1a209-a9eb-4a3f-adb6-77fbcf80bad7', 'IMAGE', 'https://cdn.chotot.com/PgHSSZNCLTPYcyHLHM8ahlryWXJsYoDN4bz8cmYWeyM/preset:view/plain/4affe3ff47d8d24476d9d18591153ac7-2996120370201216484.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('be15376a-1a54-49a6-b4ef-2ea60d825e71', 'ecd1a209-a9eb-4a3f-adb6-77fbcf80bad7', 'IMAGE', 'https://cdn.chotot.com/mpiqdvEGb0a54cH3Yx8uLSUbOo9e0gvf6F4uyDjC3Wo/preset:view/plain/99b97a2e6cdc42f0fb4a97a0f31a8a9a-2996120372665863783.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6a04f227-163b-4a68-b1ed-dc279c154465', 'ecd1a209-a9eb-4a3f-adb6-77fbcf80bad7', 'IMAGE', 'https://cdn.chotot.com/REjCJVbAYcVoZq36Mrr_wiSgp3d49XqVORHhZEpc-D4/preset:view/plain/19e680b16307429fdc70aacb6af6694f-2996120374795539752.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('60fc2c33-c1dd-4def-af7c-54dbcfb2bc20', 'ecd1a209-a9eb-4a3f-adb6-77fbcf80bad7', 'IMAGE', 'https://cdn.chotot.com/CwlHDKK0YW98QDDBi9h1KRSD1foMgGxxdHFhXgtHNrw/preset:view/plain/45bc487997ac1d9252e20aaf3dc5fcc5-2996120374898968036.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5bbc9c40-0359-4aa4-95cb-24aa7d1e86dd', 'ecd1a209-a9eb-4a3f-adb6-77fbcf80bad7', 'IMAGE', 'https://cdn.chotot.com/KOB0OlTDfFrM9WuRN14bdBO0kG9qFUmplJX6P_vohVk/preset:view/plain/ea804ef90dcd60fc0b2f15b0e641e7f8-2996120376974723449.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('0afb964f-f674-4a22-b017-7a3656f04fe5', 'P_133341063', 'APARTMENT', 'CHO THUÊ CHDV DUPLEX QUẬN 7 GẦN LOTTE MART, TDTU, RMIT, UFM', 'Dự án: Cho thuê căn hộ dịch vụ Duplex Q7, cửa sổ lớn, MÁY GIẶT RIÊNG 35m2 

Vị trí: gần Lotte Mart, TDTU, RMIT, UFM, UEL, 5 phút qua Quận 4.

Tiện ích:
- Full nội thất, MÁY GIẶT RIÊNG, cửa sổ lớn, thoáng gió
- Giờ giấc tự do, khu dân cư an ninh, yên tĩnh
- Tòa nhà thang máy, ra vào vân tay/thẻ từ

Phone/WhatsApp: *** (Jonathan Huy Tran)

ĐỒNG HÀNH CÙNG BẠN TRONG QUÁ TRÌNH "TÌM - THUÊ - Ở"

#thuephonggiare #thuetro #thuephongquan7 #canhodichvu #canhocaocap #canhoquan7 #canhoduplex #phongtroquan7 #thuecanhoquan7 #canhogiare #canhohcm #canhogiarehcm #thuetro #phongtrosinhvien #canhosinhvien #phongtrocaocap #phongtromoixay #canhomoixay #trosinhvienhcm #phongtrotphcm #phongtrodep #canhodep #canhomini #canho #canhominigiare #phongtrosinhvien #phongtrohcm', 'UNDER_OFFER', 'Quận 7, Tp Hồ Chí Minh', 40, 6000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7d161387-7b83-43a0-899d-d587086c0fab', '0afb964f-f674-4a22-b017-7a3656f04fe5', 'IMAGE', 'https://cdn.chotot.com/Wmo0p2I5pNlyNMZq_GQUNodFgCC4oPvLvoMDB01Nt8o/preset:view/plain/59e89ad7d2b049de4321bc21f4f645f5-2996122643994910808.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6dbc7ebc-74d8-47ec-b023-72aa9fd5d7b3', '0afb964f-f674-4a22-b017-7a3656f04fe5', 'IMAGE', 'https://cdn.chotot.com/HUVVZ3npbUT7SJW6oqNkKWr1C_bUl8nJpLCGvAsm-Js/preset:view/plain/9a3fe4de1f15b3bc42bbc88c6482537d-2996122645279754617.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f0cd6556-2d73-43c5-bfc7-36a38984df81', '0afb964f-f674-4a22-b017-7a3656f04fe5', 'IMAGE', 'https://cdn.chotot.com/7CfZU3YYWsDA9lLmFZdddhr_fRLNZx7BxJLLLCmPn8w/preset:view/plain/d734b17b55e6ff9a794ca5320ea3fda2-2996122648529052708.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7335e280-a08e-4114-bcf5-7038b25df1b8', '0afb964f-f674-4a22-b017-7a3656f04fe5', 'IMAGE', 'https://cdn.chotot.com/OnUxr4sDmKTxTqKU-Qq1QZwRFbjTtkGStNJZhHRn4MU/preset:view/plain/c03346fb6cb190c7fb1ac8c0bc0223a1-2996122648282091111.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2af4113f-a651-45ef-8f5c-b2c00bfa0437', '0afb964f-f674-4a22-b017-7a3656f04fe5', 'IMAGE', 'https://cdn.chotot.com/mOVK1t2AYqEMhUNsqNFQV0mmIl_IxkNUDLMa4ZMpBJk/preset:view/plain/d5d664ff86fd9b38fdfb1020675bd79f-2996122647712582009.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cbedc7cf-da54-4683-a7f2-3801aeee99ee', '0afb964f-f674-4a22-b017-7a3656f04fe5', 'IMAGE', 'https://cdn.chotot.com/KqK3YJjtXkdPIXMMnXM37eiXU5ttBuQF3OFoYiR8uSM/preset:view/plain/3e6f41466af99bcf9ec6df3a242bb633-2996122649287104665.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('ff0a0feb-073c-425d-b6e7-d22a2548af57', 'P_132916017', 'APARTMENT', 'Cho thuê 2PN đầy đủ nội thất tại Centana Thu Thiem', 'CHO THUÊ CĂN HỘ 2PN CENTANA THỦ THIÊM
Đ/C: 36 Mai Chí Thọ, Phường An Phú, Quan 2

✅ DT:64 m²- Thiết kế 2 phòng ngủ, 2 WC, BẾP, PK, logia
✅ Full nội thất: Máy lạnh, tivi, tủ lạnh, máy giặt, bếp, sofa, giường, tủ.....
✅ Giá thuê: 13 tr/tháng ( chưa bao gồm phí quản lý 540k/th)

- Tiện ích: Hồ bơi, phòng tập gym, BBQ, Winmart, ngân hàng, ATM, Phuc Long, Highland, spa, khu vui chơi trẻ em, công viên cây xanh.
👉 Nhà trống sẵn: THÁNG 7', 'AVAILABLE', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 64, 13000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0b36e352-04de-4cdb-acd2-0eb4f9537755', 'ff0a0feb-073c-425d-b6e7-d22a2548af57', 'IMAGE', 'https://cdn.chotot.com/aLgL7v5YzzNt5xusFGlIOWOlDXM-Sz6VDP-cimbqMHE/preset:view/plain/9ac96a4ffd848e9773a2404cc540254f-2988281240633190796.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('669ade8f-5388-4aff-a5b1-51353501ba70', 'ff0a0feb-073c-425d-b6e7-d22a2548af57', 'IMAGE', 'https://cdn.chotot.com/wCpqcLtYkeUHtBOFJNLNfRURzVjg8Kym8dkT7_7Hb3I/preset:view/plain/2be0aac4ffb878aaa9743e1144c084c9-2988281240352984400.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f5d28b0f-6f9a-4094-a757-e9493a4676cc', 'ff0a0feb-073c-425d-b6e7-d22a2548af57', 'IMAGE', 'https://cdn.chotot.com/gbtJNTib0niL4BPN66Li4rD3xNgua6GupyCnnop1NRM/preset:view/plain/23af0d78e1ecf67412e0790f5e3196d9-2988281240912579564.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('24ae4226-57dd-4687-b47b-c3a50a24e191', 'ff0a0feb-073c-425d-b6e7-d22a2548af57', 'IMAGE', 'https://cdn.chotot.com/KSI91xVofWmHLfI0WfCdsKWBht0-nM5dIfXw3uyFolY/preset:view/plain/2f39fd28844482d1112773baeb063232-2988281241218650625.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c3b7bd3b-63ed-4c9d-9cb3-ca40cc421285', 'ff0a0feb-073c-425d-b6e7-d22a2548af57', 'IMAGE', 'https://cdn.chotot.com/lXV_DR7rxJrWGnAy-2yijP1tpL3X5U6Z36djjZdNXE4/preset:view/plain/b4771f89064c6ba25db10d460eefde5d-2988281241211056455.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('21e03224-8738-459f-b120-7b157294af17', 'ff0a0feb-073c-425d-b6e7-d22a2548af57', 'IMAGE', 'https://cdn.chotot.com/4Y2axcmNiLzD9DFYyTZPxp2_V9AH4L6hw6FkzCdGUsU/preset:view/plain/bd9925014cd802221b6958860d782199-2988281241074470224.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1182b6c5-a678-4068-a384-0c7256807067', 'ff0a0feb-073c-425d-b6e7-d22a2548af57', 'IMAGE', 'https://cdn.chotot.com/9YPuuguPQGlHfUhuU37UFX5oJdQmyuetFwPhrPXJhl4/preset:view/plain/9d20ab1accdc696e57764318f9063ee9-2988281240939610813.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a7cd45c5-7c2f-436e-9b00-49e932956c5a', 'ff0a0feb-073c-425d-b6e7-d22a2548af57', 'IMAGE', 'https://cdn.chotot.com/93ZTFu-HtG6fUGZQdpY93wC9MdDq1kC_Bv7mycSUbjs/preset:view/plain/7f1c2f6fed4c8aadbbb32d47c7097b16-2988281240794088688.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('86abe3b3-9217-4226-86d8-25fb975707d0', 'ff0a0feb-073c-425d-b6e7-d22a2548af57', 'IMAGE', 'https://cdn.chotot.com/eYgpNw5bVADf55jfM49-TvyYRXW6eTTebcPxAZ0LiLg/preset:view/plain/f93c2ba0e50e5ef3453c5f52a987d9e5-2988281240157539308.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('068a78e1-d7de-4d78-9845-8836445c363f', 'ff0a0feb-073c-425d-b6e7-d22a2548af57', 'IMAGE', 'https://cdn.chotot.com/WGeqBcBIU1ADJC5rWBWGz56WNMU3Bxjz-NWl_7g6MlY/preset:view/plain/e8968c21c6a891efea3ed46cd75482a4-2988281240218124989.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bee68c1a-e33a-44a8-8156-df0c1b359a8c', 'ff0a0feb-073c-425d-b6e7-d22a2548af57', 'IMAGE', 'https://cdn.chotot.com/VkE3hJFZK7I0Mro9tos5D1PLyJN3P5UJ9yUyC4m72BA/preset:view/plain/428eacbc0144190d51d8c2936571f4b3-2988281240748813007.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7db9afa9-d214-4aad-83ec-b7a58658912c', 'ff0a0feb-073c-425d-b6e7-d22a2548af57', 'IMAGE', 'https://cdn.chotot.com/NK_RLkGRT1bih1vKUPpnuv8SYUy5mPUcByNxtgIG0vs/preset:view/plain/2de6d36f1501ad6cfe8337bbd4ded37e-2988281240696048338.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('911612d6-b880-44ca-bb00-87da9224a31e', 'P_133940538', 'APARTMENT', 'CHUNG CƯ MINI 1-2 NGƯỜI NGAY KHU SÂN BAY - TIỆN QUA TRUNG TÂM', 'Dự án: 
Thông tin chi tiết: ♟️𝐒𝐓𝐔𝐃𝐈𝐎 𝐁𝐀𝐍 𝐂𝐎̂𝐍𝐆 | 𝐍𝐄𝐖 𝟏𝟎𝟎%♟️
ĐỐI DIỆN CÔNG VIÊN GIA ĐỊNH - KẾ BÊN SÂN BAY

.Vị trí: Bạch Đằng, Phường 2, Tân Bình

.Toà nhà thang máy - hầm xe rộng
.Ban công thoáng - PCCC đạt chuẩn
.Ra vào tự do bằng vân tay
.Nội thất đầy đủ như hình 100%
.Giáp Phú Nhuận, Quận 3, Quận 10,… tiện di chuyển trung tâm
.Gần đại học Swinburne, Greenwich, Huflit, Văn Hiến, Học viện hàng không,…

😍Giá chỉ 4x-5x tuỳ layout phòng😍', 'AVAILABLE', 'Quận Tân Bình, Tp Hồ Chí Minh', 20, 4500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('402f144f-7c42-4019-99bd-524453150c11', '911612d6-b880-44ca-bb00-87da9224a31e', 'IMAGE', 'https://cdn.chotot.com/GQKTwUUmZL_b3C7n-Ukr2vXEpvUfa_PjEChEfomZ5wg/preset:view/plain/334230e095bf0e8e6a960a44c25fbcf3-2996121076144641320.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5015a7e5-142b-4e6b-8ba5-228e7fb36b5d', '911612d6-b880-44ca-bb00-87da9224a31e', 'IMAGE', 'https://cdn.chotot.com/zDKUQYLsbvOSVL7_weB1rI8iKV53k1kWVKwilGwtgTM/preset:view/plain/5decdbb6d6da1313f4ee37b70ddf49bb-2996121076150027748.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('977f2313-d1a9-4218-b726-493a461408a9', '911612d6-b880-44ca-bb00-87da9224a31e', 'IMAGE', 'https://cdn.chotot.com/HskJTDR64tp49gmRgJvcz99C-17kKXtNGyIXgwqL94I/preset:view/plain/18a29224ea68f7c5dd74da1f030f4b76-2996121076197073956.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('984519a6-4b0d-4bc1-8234-711377e63e8f', '911612d6-b880-44ca-bb00-87da9224a31e', 'IMAGE', 'https://cdn.chotot.com/3cpu15uIVa5wOgXKtUc6HXxt7ofG5DgAzvwUuCPrUEI/preset:view/plain/b61b8a736506b83dbd72cdec1d85679e-2996121077458995710.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('24856f3f-be0f-4bf6-a576-dcde5cc815af', '911612d6-b880-44ca-bb00-87da9224a31e', 'IMAGE', 'https://cdn.chotot.com/Ll4NhAW1cQQdTUfjj1oPOeBAMt85VhxD8-sjR2hkeoM/preset:view/plain/1887bcfc6ba20e3b7c52e1c13fee4918-2996121076226345337.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4f2aa1c3-8e7d-4d74-ac09-32e109ea4592', '911612d6-b880-44ca-bb00-87da9224a31e', 'IMAGE', 'https://cdn.chotot.com/b11NXzckYc2O5Qjk8GdUfjlobgabDEYHyuMlazOOdSo/preset:view/plain/01c65b0db80023558b3d5ae90760a041-2996121076304989799.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('36afc9e6-53e5-4498-b30c-c6fc6fbb164b', '911612d6-b880-44ca-bb00-87da9224a31e', 'IMAGE', 'https://cdn.chotot.com/GjHsz1gBCEHmL9t4HxJzVhXllMl0_C1DkmAQdi-natY/preset:view/plain/7fff041bc15d4b43d28bedfbca7b7f2f-2996121076735529983.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('626e2db0-b76f-4289-b044-73b2c2356b31', '911612d6-b880-44ca-bb00-87da9224a31e', 'IMAGE', 'https://cdn.chotot.com/Tab8YNRlu0XTUxrfTizQ7out7OXTLA_1Bt5ECCb0md0/preset:view/plain/db32f19283f9ce581a96eb4910051976-2996121076387850095.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1c862dfe-b11c-4642-a808-aeb0e47f2ffa', '911612d6-b880-44ca-bb00-87da9224a31e', 'IMAGE', 'https://cdn.chotot.com/0u2C_sVvtev4FwtHAkF3K0chJXkxLb-H9mwl5cWnMFc/preset:view/plain/ebd78c5027eb35b66601df3deacbea7f-2996121077327632537.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5cd05ebd-2e2d-4eb9-829e-9311fdcc2d67', '911612d6-b880-44ca-bb00-87da9224a31e', 'IMAGE', 'https://cdn.chotot.com/yvAjvX1hO_6XaC1AP-4fA2zwE1xBFvt20h5TOsN1fyY/preset:view/plain/70016d31586c2180b85b708a6dab0f2b-2996121076591025047.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f2be3651-46e9-43a0-8c61-2de7f1dbe025', '911612d6-b880-44ca-bb00-87da9224a31e', 'IMAGE', 'https://cdn.chotot.com/kCZhh_z9SKRKwFpXUuaQ_Dhag0SaFW5H-C3WArDTexA/preset:view/plain/c4f443f68bae24d44c37c5c2094b832c-2996121076976556113.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b7a0222f-65ee-40e5-84f1-2c6f32d5de3b', '911612d6-b880-44ca-bb00-87da9224a31e', 'IMAGE', 'https://cdn.chotot.com/r8gL6cTuaU-i4f3ZqXrbQdku7aVGwRP5LbEiySz8EWE/preset:view/plain/4c82fec9825e006f39d0feb2a7cd5964-2996121076422811736.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('ebfc9c0a-ff0e-43cb-b28e-ed26786e260d', 'P_133940519', 'APARTMENT', 'Cần bán căn hộ Ehome 2 có balcon', 'Cần bán căn hộ Ehome 2 - Phước Long B cũ
Nằm trong KDC Nam Long- cách Global City 1km
Thuận tiện di chuyển lên Quận 1- Quận 2
Căn tầng cao view thoáng, hướng Đông Bắc
Diện tích: 66m2-2PN- 2WC- ban công đã cải tạo rộng thoáng
Để lại toàn bộ nội thất dính tường
Căn hộ đã cải tạo, thay mới toàn bộ sàn gỗ, sàn gạch- thiết bị vệ sinh
Giá có thương lượng hỗ trợ khách vay
Làm việc chính chủ ạ ❤️❤️❤️', 'UNDER_OFFER', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 66, 2950000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('60fb1d4f-dbe6-4025-9a83-f5bcd3d2df70', 'ebfc9c0a-ff0e-43cb-b28e-ed26786e260d', 'IMAGE', 'https://cdn.chotot.com/Lw_ufVM2QLaaJXVw_UVao43js13r_Vb5OFzw1HC7ZlA/preset:view/plain/21e3bbbbcd8cc22ca2f505ebc1db8367-2996121477101241828.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a6d35e7a-06db-4bf8-9984-395a6d566ba9', 'ebfc9c0a-ff0e-43cb-b28e-ed26786e260d', 'IMAGE', 'https://cdn.chotot.com/ygituZN4AwO1OlRc8TQCMz7uf8WOpdi6cWEtz2ZNISQ/preset:view/plain/055c0daad0f0b224c10eb61ebe90372e-2996121477478107513.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('72fc006a-3add-49f9-bb4b-53fa752dfd79', 'ebfc9c0a-ff0e-43cb-b28e-ed26786e260d', 'IMAGE', 'https://cdn.chotot.com/pnp4yz0Tce1RMDwicUDonhkpGI2SD6eRP_qRUf4NHKE/preset:view/plain/c262c9644fdee65c9e2444d4cb69706f-2996121478017164008.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f57158ae-a2ff-4e02-91e2-3a8e4dbd1223', 'ebfc9c0a-ff0e-43cb-b28e-ed26786e260d', 'IMAGE', 'https://cdn.chotot.com/Kqon8omacDHV8MkCnNj1wAxANNlrguM_0tXvkYH-Ce4/preset:view/plain/f5f5dce24695213adc5fbf37291cdf73-2996121477683707405.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0c3300d7-73c8-4d4b-9900-f770b20ab601', 'ebfc9c0a-ff0e-43cb-b28e-ed26786e260d', 'IMAGE', 'https://cdn.chotot.com/hmpQ_6MKZ2QGA4QuRt0YI13aX49Eh0Sh9HaylECMG0s/preset:view/plain/56aca73a872322d21126a1a2fa96a0b3-2996121478418044806.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d7887807-2f28-4c1f-b6d0-7f106eb8718a', 'ebfc9c0a-ff0e-43cb-b28e-ed26786e260d', 'IMAGE', 'https://cdn.chotot.com/snLcu5yB5JFlr_nOPhXrR__IQ01otMycqBZERthMSVc/preset:view/plain/ab44fdb090f145c946b972be06a8c598-2996121478233771716.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('eec31931-1fb7-49c1-9887-c5cf6d3ce792', 'P_133940497', 'APARTMENT', 'CHO THUÊ 1PN PEGASUITE -  FULL NỘI THẤT GIÁ 9,5 TRIỆU', 'Dự án: 
Thông tin chi tiết: CHO THUÊ 1PN FULL NỘI THẤT GIÁ 9,5 TRIỆU 📍 Địa chỉ: 1079 Tạ Quang Bửu, Phường 6, Quận 8, TP.HCM _________________________________________ 🏢 𝐓𝐇𝐎̂𝐍𝐆 𝐓𝐈𝐍 𝐂𝐀̆𝐍 𝐇𝐎̣̂  ▪️ Diện tích: 52m² ▪️ Giá thuê : 9,5 Triệu/Tháng  ✅ Đăng hình thật - xem nhà thực tế  __________________________________________ 📞 𝐋𝐢𝐞̂𝐧 𝐡𝐞̣̂ 𝐧𝐠𝐚𝐲 đ𝐞̂̉ 𝐱𝐞𝐦 𝐧𝐡𝐚̀ 𝐭𝐡𝐮̛̣𝐜 𝐭𝐞̂́:', 'SOLD', 'Quận 8, Tp Hồ Chí Minh', 52, 9500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2c0bf089-50be-48bf-811e-bba3be878be1', 'eec31931-1fb7-49c1-9887-c5cf6d3ce792', 'IMAGE', 'https://cdn.chotot.com/HIn3n1ax5fHC8d8Yo8iPaAtqr0GneHNABRKwSoESkv0/preset:view/plain/a36229640f4a226a752d198d344f8942-2996121462152283620.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c3bf4d4e-017c-4239-ae0b-8c35204e8d01', 'eec31931-1fb7-49c1-9887-c5cf6d3ce792', 'IMAGE', 'https://cdn.chotot.com/d1WfcxqWOIEj73SzXwDOoaiR2LfqfjQD9TePowtm4q0/preset:view/plain/19943e154c201100407049d4318b835e-2996121462243871097.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d672a2ae-b54c-4e49-9236-1ed70f976939', 'eec31931-1fb7-49c1-9887-c5cf6d3ce792', 'IMAGE', 'https://cdn.chotot.com/TH-A8297BuRbTHwoljNajOnT2WcLkQiuPx-yMzlyrO4/preset:view/plain/8ffc34e640e72fc68b129adddc673690-2996121462229804068.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4f6f9fce-476b-4278-a904-1ae67c6f84a5', 'eec31931-1fb7-49c1-9887-c5cf6d3ce792', 'IMAGE', 'https://cdn.chotot.com/HaWGUwXT0pfxiSiSTorTbEBhaQxiQT4ONBUmIJh0YAg/preset:view/plain/13e2e3292d5c55103ff6575b1ab374a8-2996121462278640639.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('7ca31a1b-885f-4159-b0b0-fd15c6658c1d', 'P_133940489', 'APARTMENT', 'Căn hộ gác 1m5, chỉ cho nữ ở, HÌNH THẬT', '
✔️ Thiết kế hiện đại, sang trọng, không gian sáng – thoáng – sạch
✔️ Ban công rộng, cửa sổ lớn, đón gió và ánh sáng tự nhiên
✔️ Bếp full tiện nghi, đầy đủ thiết bị nấu ăn
✔️ Tòa nhà cao cấp với lễ tân – bảo vệ 24/7 – thang máy – hầm để xe
✔️ Khu vực trung tâm Quận 1, thuận tiện di chuyển đến mọi quận

', 'AVAILABLE', 'Quận 3, Tp Hồ Chí Minh', 35, 5500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c55eb969-5fed-4955-8a52-b6843ff95ec3', '7ca31a1b-885f-4159-b0b0-fd15c6658c1d', 'IMAGE', 'https://cdn.chotot.com/ZFUby8gu-RCJSwmq-EBznh0ZSSYXaT-4FQF8kLnIQJc/preset:view/plain/d0724a2ec84e83d97836969c03545445-2996121334357607908.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9f046e32-4b71-4b8a-843b-c9a8b20ca510', '7ca31a1b-885f-4159-b0b0-fd15c6658c1d', 'IMAGE', 'https://cdn.chotot.com/dmy0RyU8RBqCQaxEyb4J7kfY_s5BPfEQwy1gRgwAfhU/preset:view/plain/d118b5dd717edf97268bcc05835ff5ec-2996121361347224612.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4f89843d-5583-4856-b2c3-d28f8ad748e6', '7ca31a1b-885f-4159-b0b0-fd15c6658c1d', 'IMAGE', 'https://cdn.chotot.com/Rjr-HXcWpiQaMkfmUQIvTNVt-2iya-7t1V4JOkuHhFI/preset:view/plain/470036f1f81f6c60269753bcefecfacb-2996121361453555800.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('07ace3b5-6498-463a-8b6f-efef5af9608b', '7ca31a1b-885f-4159-b0b0-fd15c6658c1d', 'IMAGE', 'https://cdn.chotot.com/pzZcjL_OLcDx9WOKnLJfjSrjFqKgxl8JXlBtEWRGaWU/preset:view/plain/44e124d8d3a967de0749edcea19d5ced-2996121361453955821.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('38fb28d2-0788-479e-afba-36abec7a8925', '7ca31a1b-885f-4159-b0b0-fd15c6658c1d', 'IMAGE', 'https://cdn.chotot.com/WjuGQJI95BCMfoigeF0nnYplDipsCzbtozd55ogjn9Y/preset:view/plain/57ff637899b1a2bb3a29d23b4f028279-2996121361665283071.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('72761539-b15c-4942-ac2c-205073d542e3', '7ca31a1b-885f-4159-b0b0-fd15c6658c1d', 'IMAGE', 'https://cdn.chotot.com/ck6TAQWUssc89KueJrzPiuGk2RLF7ul9NxL9DOO58KU/preset:view/plain/0f3b6b05fd46de8ab4e9aa5d66d631ff-2996121361518317159.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('9366e080-911a-48d3-8ab9-99d3ad81993f', 'P_133725601', 'APARTMENT', 'cho thuê căn 3pn đường Nguyễn Văn Thương', 'Cho thuê nhà sửa mới toàn bộ, 3 phòng ngủ, 1 phòng khách, 1 bếp, 1 WC (16/42 Đường Nguyễn Văn Thương, P25, Q.Bình Thạnh) giờ giấc tự do thoải mái
• Hẻm xe hơi đi được, ngay chợ, gần Pearl Plaza, gần trường Hutech, uef, hồng bàng có thể đi lại thuận lợi, an ninh tốt
• Đặt cọc tối thiểu 2 tháng
• Tiền internet trả theo gói, Tiền điện nước tính giá nhà nước

***Liên hệ chủ nhà: Cô Chi ***
', 'AVAILABLE', 'Quận Bình Thạnh, Tp Hồ Chí Minh', 50, 8000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('28a61f3d-bdf5-455d-a5cb-e4c39cc69031', '9366e080-911a-48d3-8ab9-99d3ad81993f', 'IMAGE', 'https://cdn.chotot.com/H2MJ_Yb08RmdP4erBri9NncqTCn4BVfA_hFstDW4FXA/preset:view/plain/4cc08729f8a7fce59d458e89fdb7b3e8-2994498330837252851.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a400b188-73d0-4ade-8c57-c1b87073175b', '9366e080-911a-48d3-8ab9-99d3ad81993f', 'IMAGE', 'https://cdn.chotot.com/5HeeSHQjxF2dy8T-Bpe4dg-jLu0NwveqAo7_RG4FKK0/preset:view/plain/901185c7b1191c9efdc0f63452b5dbfe-2994498330965026415.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7da9c0df-ccb5-4be2-9d2a-464f74df44fa', '9366e080-911a-48d3-8ab9-99d3ad81993f', 'IMAGE', 'https://cdn.chotot.com/JY-zueB3--zs_d8gwkjGaVUHtSLLW-U1C2PPjKyk9FQ/preset:view/plain/e66486c312dd868edc2d1fe27a405507-2994498331892241264.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a795837f-ba53-4047-a11a-4b067b941113', '9366e080-911a-48d3-8ab9-99d3ad81993f', 'IMAGE', 'https://cdn.chotot.com/s1UvP9lp8kbthgwNSU_da688fheKlaYNuDDiOq7RnVk/preset:view/plain/890395a42a2a6b64164c9da5e2bddfa6-2994498331861051649.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('3d7de6d6-723b-40ad-a385-414cdc78f2db', 'P_110551247', 'APARTMENT', '🌇🎉Khai Trương Căn Hộ Thảo Điền Mới 💯Ban Công Quận 2 Gần Cầu Sài Gòn🎉🌇', 'Hỗ trợ tìm phòng quận 2 đầy đủ tiện nghi, đáp ứng mọi nhu cầu cho mọi đối tượng khách hàng ( sinh viên, nhân viên văn phòng, khách nước ngoài thuê )
🆘🌸- Đầy đủ nội thất, trang bị thiết bị hiện đại, tiết kiệm điện ..
🌸- Vị trí thuận tiện di chuyển, chỉ 5-10p qua Bình 🌸Thạnh, quận 1,3,7 , các quận trung tâm sài gòn
🌸- Giờ giấc tự do, không chung chủ
🌸- Ra vào có vân tay, di chuyển bằng thang máy
🌸- Gần chợ, siêu thị, trạm xăng,...
🌸- bảo vệ 24/24 bảo đảm an ninh
🌸- chỗ Để xe siêu Rộng
🌸- Nhiều tiện ích, A-Z KHÔNG THIẾU GÌ
🌸- Chỉ tính điện nước, còn lại free
🌸 đủ dạng PHòng Tại Quận 2
💯 Loại phòng:
- Studio full nội thất: 5.000.000 - 9.000.000
- Gác full nội thất: 6.500.000 - 8.000.000
- 1PN: 7.500.000 - 16.000.000
- 2PN: 11.000.000 - 22.000.000

☎: Call/zalo ( Chỉnh) để được tư vấn và xem phòng. ( hỗ trợ tìm phòng khu vực quận 2', 'AVAILABLE', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 50, 10000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a6bb81eb-8aff-43d9-9373-b1ad631acbe3', '3d7de6d6-723b-40ad-a385-414cdc78f2db', 'IMAGE', 'https://cdn.chotot.com/WYCfNZZtM-x-EM5O96vYXs2oYoyIOSv408FAhoBwrdE/preset:view/plain/b4ce530b769687b2ffd767e124f63e5a-2846352005363494356.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3496dbaa-41ac-4492-afbd-5e1b2f957e05', '3d7de6d6-723b-40ad-a385-414cdc78f2db', 'IMAGE', 'https://cdn.chotot.com/rCCwT0W8KdfUbKuH9uQb0wouNuSJCpofVAQM03puejo/preset:view/plain/f2299cb2efb40262bc0ead422e1dabbb-2846352005715494222.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7e92e8ee-92c9-4580-9d09-c98b111987dd', '3d7de6d6-723b-40ad-a385-414cdc78f2db', 'IMAGE', 'https://cdn.chotot.com/JNZVYSCveHIqxA3W5VsyGag_PKishDpxGmAU8Y2iII0/preset:view/plain/5046a98c8f40fb86b151d709ad61bc3e-2846352006007872417.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('20901926-d3d0-4e75-8b13-e3e7d7bd628d', '3d7de6d6-723b-40ad-a385-414cdc78f2db', 'IMAGE', 'https://cdn.chotot.com/eQrlhb4BrQjgLHF-OVgOTLg1DBfVIN9KcprPeYHfhWc/preset:view/plain/ecede7d6a7a1d50de850386a2ab94931-2846352006183173226.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('39382447-11f3-4777-8896-613bd01a3c16', '3d7de6d6-723b-40ad-a385-414cdc78f2db', 'IMAGE', 'https://cdn.chotot.com/8HOdB_70GWPB4IwCt28eP8li7zrnkl3Me2gGPnb6n1c/preset:view/plain/8b0dd484f20f900340a7ff86e05e22f1-2846352006538951034.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('403429ff-a85a-4f03-abf6-7c24fe2add83', '3d7de6d6-723b-40ad-a385-414cdc78f2db', 'IMAGE', 'https://cdn.chotot.com/l5YBffW6wCLOJklfBECZHPeFKr0N47_2kISOH9fyFd8/preset:view/plain/6f8b4fb46ce6644d68d8eb75ca08db1a-2846352006273039870.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('30ed5b62-9b87-4394-b60d-741ed966fc55', 'P_133940475', 'APARTMENT', '🚨CHDV MỚI XÂY GẦN ĐH VHU 7P DI CHUYỂN - NT MỚI - GÁC CAO CỬA SỔ TRỜI✨', 'Phòng Nằm trên đường LÝ THÁNH TÔNG dành cho các bạn Sinh Viên Học tại VHU . 

📍LÝ THÁNH TÔNG - PHÚ THẠNH. 

TIỆN ÍCH PHÒNG:
• NT mới Gồm : Máy lạnh - tủ đồ - kệ bếp.... 
• Gác cao Không đụng đầu.
• Cửa sổ trời thoáng mát. 
• Ở 2 - 3 người vô tư
• Khoá Vân tay. 
• Không chung chủ. 
• Camera an ninh. 
🛵Thuận tiện di chuyển : ĐH VHU - Chợ - Trục đường lớn - Các quận trung tâm - Quán ăn - Coffe - Gym - Siêu thị ...', 'SOLD', 'Quận Tân Phú, Tp Hồ Chí Minh', 30, 4000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a5a916f1-03e4-4f3f-9d2b-9edddb17f465', '30ed5b62-9b87-4394-b60d-741ed966fc55', 'IMAGE', 'https://cdn.chotot.com/91E1FmfLUBsxI9hI1uprW3QpL5pr62LNeNA37tnC49k/preset:view/plain/8562724c597c4bc35f980c4b66f34aca-2996121318630659368.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('95174826-be7c-4641-8dd0-af06fd0154c9', '30ed5b62-9b87-4394-b60d-741ed966fc55', 'IMAGE', 'https://cdn.chotot.com/8rTJhrk8NOUBFlC8etwkn7Glr11E0Yjjk14tq-Zdq-k/preset:view/plain/fe34ab4332f41e3c982caea361e712e6-2996121318838355428.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5af75c54-8257-42c3-a493-8646ac2e7684', '30ed5b62-9b87-4394-b60d-741ed966fc55', 'IMAGE', 'https://cdn.chotot.com/J7g7RfJ43Le2AKB-sZq1Ldw-S1G9f01wbdQdEMAR9gg/preset:view/plain/58c392904bc3ef89d84d0bb1af8bd747-2996121319903021433.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('277ec2a8-76cf-4200-b3d2-88b3241b23fa', '30ed5b62-9b87-4394-b60d-741ed966fc55', 'IMAGE', 'https://cdn.chotot.com/78EOOyvJKzG0bBcUaZnmRUGP9BasZt8x9Nevi5ttWhs/preset:view/plain/4308051c84c6be6d451a92d52b8deae0-2996121320241337640.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6bf55320-987f-4bb6-95be-83f02a544707', '30ed5b62-9b87-4394-b60d-741ed966fc55', 'IMAGE', 'https://cdn.chotot.com/dgRRvZhUI8yn6CFX9aZH_at8CtsJyrX8i5EHv_hix3E/preset:view/plain/27c4a01922d6661faa39060503714465-2996121321432585512.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('88d5e9f7-fee7-4880-898c-53760690ca0f', '30ed5b62-9b87-4394-b60d-741ed966fc55', 'IMAGE', 'https://cdn.chotot.com/vgJxUWo5acm3Pw7qCL5gSBQygXDdLHudm38rFJPnSSc/preset:view/plain/f88d98ab78711cefc4e3ccc22223d48c-2996121322338833407.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f90d4381-874f-4dca-a62b-1c6168374c4c', '30ed5b62-9b87-4394-b60d-741ed966fc55', 'IMAGE', 'https://cdn.chotot.com/kfjObubDIPfw-tvk2DVIO8gNeURJfSXhSQT_WWfOp9M/preset:view/plain/ce8d25b6222c64bddd55e62f805ce474-2996121323493411193.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('24ce7e7a-19b8-49ea-a6dd-1e3a4828ef56', 'P_133940462', 'APARTMENT', 'Căn Hộ Cityland 3pn 2wc full đẹp căn góc 114m2 giá tốt 7,4 tỷ ', '🍍🍍🍍BÁN RẺ CĂN GÓC CITYLAND PARK HILLS – SỔ HỒNG LÂU DÀI 🔥
🏡 Diện tích: 114m² – Căn góc cực thoáng
🛏️ 3 phòng ngủ – 2 nhà vệ sinh
✨ Full nội thất đẹp, chỉ xách vali vào ở
📜 Sổ hồng lâu dài – pháp lý rõ ràng
💰 Giá chỉ 7,4 tỷ – Cơ hội sở hữu căn hộ rộng đẹp với mức giá cực tốt!
✅ Căn góc đón gió, ánh sáng tự nhiên
✅ Không gian sống rộng rãi, phù hợp gia đình nhiều thế hệ
✅ Khu dân cư cao cấp, an ninh 24/7, đầy đủ tiện ích: hồ bơi, gym, công viên, siêu thị...
📞 Liên hệ ngay: để xem nhà thực tế và thương lượng trực tiếp với chủ.', 'AVAILABLE', 'Quận Gò Vấp, Tp Hồ Chí Minh', 114, 7400000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b6614116-6bdf-4057-8fdb-ebbe3d38de5a', '24ce7e7a-19b8-49ea-a6dd-1e3a4828ef56', 'IMAGE', 'https://cdn.chotot.com/kC4jHDs03a9tKATFTyv9IxYdWnhazr3hKp9W6vRf4ZE/preset:view/plain/8c9145b205606671d25fbec338cd6c42-2996121135459875565.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('79bb6427-5b73-4ef6-921e-fe7a850d8eaa', '24ce7e7a-19b8-49ea-a6dd-1e3a4828ef56', 'IMAGE', 'https://cdn.chotot.com/o2ZjGpHWIKn1qICPcwB6D36zAE8ITNO8wUpmbu9eiGQ/preset:view/plain/7cfefc43b9e0f05bd017dea659e4a27b-2996121135534852473.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0b6087c7-8b62-4a4a-98cf-50b9665ffdd0', '24ce7e7a-19b8-49ea-a6dd-1e3a4828ef56', 'IMAGE', 'https://cdn.chotot.com/uX2aN85LdgENoY1dTG8R_0ITvgvvAbADw7148nNrkDQ/preset:view/plain/0f0c9a2c27ae674c20a22c8785aaf0ec-2996121136733996516.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b4421641-7438-4979-9dce-786941654747', '24ce7e7a-19b8-49ea-a6dd-1e3a4828ef56', 'IMAGE', 'https://cdn.chotot.com/9_fMhG_fWq6kUoDIBAKYe8LcqBW_kw0mMtB44dHl5Nw/preset:view/plain/3d1441d903125d8d7af24afa489d88ac-2996121136510244136.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d4ad3e4c-91ab-4480-9051-e6bf0ca12b1c', '24ce7e7a-19b8-49ea-a6dd-1e3a4828ef56', 'IMAGE', 'https://cdn.chotot.com/M32csE-fBvieGegiXQI41d1aYdoH0cle2GaKwni0Xr0/preset:view/plain/86a2771afa4b6586cc2b6b61f691e6c3-2996121137690363364.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('feb907c9-16d3-4f6a-89bb-360cfbdb12bb', '24ce7e7a-19b8-49ea-a6dd-1e3a4828ef56', 'IMAGE', 'https://cdn.chotot.com/NtDrKhdExKjH-xCiedaaTpF4KU-2dsHn_NHI1RFOawU/preset:view/plain/224d02c3aaacaab7a9ccda7d17f64487-2996121138012364888.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('b4176a26-8d03-4c73-982f-c40ac4257faf', 'P_132827065', 'APARTMENT', '🔥CHDV Mới Khai Trương Q3–Full Nội Thất Cao Cấp,ngay Hồ Con Rùa', 'Dự án: 
Thông tin chi tiết: 🔥 GIẢM SỐC 500K CHO KHÁCH THUÊ VÀO Ở NGAY! 🔥
🏡 Căn hộ dịch vụ cao cấp tại Võ Văn Tần, Quận 3 – vị trí trung tâm thuận tiện di chuyển đến Quận 1, Bình Thạnh, Phú Nhuận và các khu vực lân cận.
✨ Nội thất đầy đủ, hiện đại:
✔️ Giường nệm cao cấp
✔️ Máy lạnh, tủ lạnh
✔️ Tủ quần áo rộng rãi
✔️ Khu bếp tiện nghi
✔️ WC riêng sạch sẽ
✔️ Ban công thoáng mát, đón ánh sáng tự nhiên
📍 Gần Chợ Bến Thành, Hồ Con Rùa, Nhà thờ Đức Bà, Dinh Độc Lập, phố đi bộ Nguyễn Huệ và nhiều trường đại học, văn phòng trung tâm.
🎁 Ưu đãi đặc biệt: Giảm ngay 500.000đ cho khách chốt thuê và vào ở liền.', 'AVAILABLE', 'Quận 3, Tp Hồ Chí Minh', 35, 6500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('af38a585-fd09-45dd-9a91-ec6d113ae896', 'b4176a26-8d03-4c73-982f-c40ac4257faf', 'IMAGE', 'https://cdn.chotot.com/Wy87gp85rP7paUU8LFFPpKlpgjp0GMbXzf_b_dcVp7k/preset:view/plain/93f8c93afe7e93b3be32a3d48e5e09fa-2987590879938790403.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('96381b48-ac1b-4155-acb7-92c5a69f7a12', 'b4176a26-8d03-4c73-982f-c40ac4257faf', 'IMAGE', 'https://cdn.chotot.com/5jcGhdEpHind-vrx1qUgy5hydAORZv0xAqy82MByKkE/preset:view/plain/63c1fb675902b1f3923e5ad647558717-2987590879873395407.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('88c01dd3-2889-49f1-ab6d-4f6b274138f8', 'b4176a26-8d03-4c73-982f-c40ac4257faf', 'IMAGE', 'https://cdn.chotot.com/H5tVBhEWxFMQ_7ltWWLpUC8tkASvzHUPs7HU6A-PG0I/preset:view/plain/9e6fa7fccdacb888985a3fe67ec9ab2c-2987590879886912878.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('26ba3918-b865-49d5-bfc5-866750089f97', 'b4176a26-8d03-4c73-982f-c40ac4257faf', 'IMAGE', 'https://cdn.chotot.com/FOvb79c1dw9um-UGA4bAB_j2VNTnslTgwk0L0hQw4Aw/preset:view/plain/08bf34a43acf071ed502b6b3757a72cf-2987590879941034018.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0cafab1e-6279-4198-9329-82c6fb90536f', 'b4176a26-8d03-4c73-982f-c40ac4257faf', 'IMAGE', 'https://cdn.chotot.com/c-yNAWTjjSlJkHHuF2Yc8WwI1QVd_Iz_DS7hENkzOpM/preset:view/plain/3658e7e20e8a279350e88b6ba92eb95c-2987590879898431071.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0815b546-1c22-4b24-bb65-5a941d75525f', 'b4176a26-8d03-4c73-982f-c40ac4257faf', 'IMAGE', 'https://cdn.chotot.com/cZ-gANsziMzYaHWNkF3AaMSnH_leb3XtTX4jtulWO-8/preset:view/plain/a2def4fdce45f4d9a7d2db9de66682fd-2987590879978878103.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b6c6937c-44fb-432b-b14d-7ec15ef18dcd', 'b4176a26-8d03-4c73-982f-c40ac4257faf', 'IMAGE', 'https://cdn.chotot.com/VSwOICTNhkm0LcWXjyWXJ-haJsbw2wrpYVY9x8Ug-oI/preset:view/plain/d8d13447710fbed7932ec66c35c31e17-2987590879846605839.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('26c25115-d4ee-495d-a59e-6b9283f8deb1', 'b4176a26-8d03-4c73-982f-c40ac4257faf', 'IMAGE', 'https://cdn.chotot.com/gHr9ePoBD88HqJD05gMuBPXdXWjoEYC3dn_8nqbUKj0/preset:view/plain/b90e19fcf32127ab3ab5ed2618beb4b4-2987590879963293438.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('770265bc-a8b5-4976-b9e3-23df14bfc927', 'b4176a26-8d03-4c73-982f-c40ac4257faf', 'IMAGE', 'https://cdn.chotot.com/kQ98OaD-ue-EBHT09-QeDKruZDPWE_08ePOyVVpuYDs/preset:view/plain/f0f99c70123b235cd0377479a53930ee-2987590880224988652.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6a03d866-7ae9-4b17-8a4b-2a01adc37c75', 'b4176a26-8d03-4c73-982f-c40ac4257faf', 'IMAGE', 'https://cdn.chotot.com/xSVIplRXfTrHSocNI8CBOFj_-seiZN6pLJu95N1uh-k/preset:view/plain/59b7a391df316fa5f2f7be5716cf1981-2987590879929259677.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('5fc0df02-5012-4410-bed2-d8ca5cb0b576', 'P_133612624', 'APARTMENT', 'Bán Căn hộ đã có sổ hồng sầm uất nhất nhì Tạ Quang Bửu', 'Dự án: 
Thông tin chi tiết: Cần bán gấp căn hộ chung cư The Pegasuite
Mặt tiền Tạ Quang Bửu
Full tiện ích , shophouse, công viên, siêu thị
Hồ bơi chuẩn thi đấu
——
Căn hộ thiết kế 2PN 2WC : 68m2
Đã có sổ hồng 
Hỗ trợ vay ngân hàng
Sẵn chìa khoá xem nhà
——
Liên hệ : Phương xem nhà 24/24', 'AVAILABLE', 'Quận 8, Tp Hồ Chí Minh', 68, 4400000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d244d08a-9f4b-4b3a-bcdf-ba5593ff3341', '5fc0df02-5012-4410-bed2-d8ca5cb0b576', 'IMAGE', 'https://cdn.chotot.com/8ZxNlzAStsMV9WmTrmCsNwxtvHQKBj4aQPj3GNf834Y/preset:view/plain/25473d93ed0cab7cce7a8124b5f2f90b-2993629039824134154.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5cae3150-cf34-4458-bb93-cf104ae81e81', '5fc0df02-5012-4410-bed2-d8ca5cb0b576', 'IMAGE', 'https://cdn.chotot.com/gf2XzURKgRbcpyqjB8Obp0pvrGcvf_A1qCV8luOJ1es/preset:view/plain/b330a953cae6de1d849fde8aa1d17838-2993629040148487346.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3d1c1aff-b663-4619-a2c9-2499326c80dd', '5fc0df02-5012-4410-bed2-d8ca5cb0b576', 'IMAGE', 'https://cdn.chotot.com/9gw1wZdTaoFGpu-DzGI_oEW1i4R7X_F-WAl6g0zqT1w/preset:view/plain/462bfb41f005704bd05424a7e115825b-2993629039845126382.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ff995457-d87d-4a06-bd22-0ca36a2449b2', '5fc0df02-5012-4410-bed2-d8ca5cb0b576', 'IMAGE', 'https://cdn.chotot.com/5A3KS1qqP8lmx8aa1FhDTTTxkAygQwZveJ-hjjsA0-o/preset:view/plain/08f0d8a02011627ca0b31e2fc3868d0f-2993629040016689909.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f07a9d77-ea2f-46bc-b0b6-cba00bf19fb9', '5fc0df02-5012-4410-bed2-d8ca5cb0b576', 'IMAGE', 'https://cdn.chotot.com/JaRhwFW0SjzOFz-FDhbQrQeNFriC-knJbWRhASXCsMw/preset:view/plain/f5b8b61d96985fc315d18973e71af25a-2993629039989456396.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7c5df960-e693-4e7a-b4ce-30315792a71c', '5fc0df02-5012-4410-bed2-d8ca5cb0b576', 'IMAGE', 'https://cdn.chotot.com/cAbhmgImxVCPNtVKuKFZ8yRd6-IkE4r3LtcfoVse5kI/preset:view/plain/e7136264702d538a680d259077f088e8-2993629040058999107.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d641c172-3ca8-4cdd-8947-a0413ed860f3', '5fc0df02-5012-4410-bed2-d8ca5cb0b576', 'IMAGE', 'https://cdn.chotot.com/wWv7z_50jeyLcpJc94jWjazZ2Z1pvSPOsbxWKvMpv88/preset:view/plain/04ddb4f59f724877749450d07481d552-2993629040105878484.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f96ce67f-d69e-44b7-965e-1512fd3c6b81', '5fc0df02-5012-4410-bed2-d8ca5cb0b576', 'IMAGE', 'https://cdn.chotot.com/fBIXuyBFWOHTV9kqOmoVb2JtMle22CLJtBKy0hP-Pms/preset:view/plain/d33464c36dfa9104cb3353a73b1959df-2993629039972939719.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e1af8333-34af-4974-8dd2-fd89f9d76c22', '5fc0df02-5012-4410-bed2-d8ca5cb0b576', 'IMAGE', 'https://cdn.chotot.com/oStYdILtL1AgY_IddQkpsyjSnOcM2lGHkbSvcKtf9Tg/preset:view/plain/f19e54cbc9454d5f306d303f6bb0304e-2993629040020152154.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('1480cfe4-3536-410a-8b64-0a4ca18f9113', 'P_133940457', 'APARTMENT', 'Chính chủ bán CH Green River Q8, DT 65m2/ 2PN, nhà mới, giá 2.77 tỷ', 'CHÍNH CHỦ BÁN CĂN HỘ GREEN RIVER - MẶT TIỀN PHẠM THẾ HIỂN, QUẬN 8
- Diện tích: 65m²
- Thiết kế: 2 Phòng ngủ | 2 WC
- Giá bán: 2.77 tỷ VNĐ (Chưa bao gồm thuế TNCN và sổ)
- Pháp lý: Sang tên công chứng ngay
🌟 VỊ TRÍ & TIỆN ÍCH NỔI BẬT
- Vị trí đắc địa: Mặt tiền đường lớn, di chuyển sang trung tâm chỉ 10 - 15 phút.
- Tiện ích nội khu: Trung tâm thương mại và siêu thị ngay dưới tòa nhà.Khu sầm uất: Hàng chục quán cà phê, nhà hàng, cửa hàng ăn uống sát vách.
- Đánh giá: Vị trí đẹp, mức giá quá rẻ so với khu vực ở thời điểm hiện tại.
📞 LIÊN HỆ XEM NHÀ TRỰC TIẾP
Liên hệ: Ms Nhung
Gọi điện trực tiếp hoặc nhắn tin Zalo.', 'AVAILABLE', 'Quận 8, Tp Hồ Chí Minh', 65, 2770000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('48710e82-3b33-4098-babb-df16d6208cb8', '1480cfe4-3536-410a-8b64-0a4ca18f9113', 'IMAGE', 'https://cdn.chotot.com/3s6zvJqjjP1j0z9nRmk-Q66xKx6y-1Er1AUIZ5aE1Sk/preset:view/plain/9b41018c5372f58899ebeeb272851136-2996121174743730553.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('226bab40-3ec2-4a21-bf68-f4b6ed20d3b3', '1480cfe4-3536-410a-8b64-0a4ca18f9113', 'IMAGE', 'https://cdn.chotot.com/SS4LVzKH9GXVaFFNdROQF0yYpIeaPWr8SNmLWHzaO6I/preset:view/plain/68001ec2c2d4d6a27e719196191166b4-2996121194264869613.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('85c13ee2-699c-427e-8c8e-a029bd34f208', '1480cfe4-3536-410a-8b64-0a4ca18f9113', 'IMAGE', 'https://cdn.chotot.com/9wVtorgjmcxuOuSdatOTrfkAXrXu8Lf5lkFk5rrNevc/preset:view/plain/7bfafd8a1b25d466abfe26539a892690-2996121194377356324.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('eb22412f-6f81-497b-b2c0-aae2ca1f53d3', '1480cfe4-3536-410a-8b64-0a4ca18f9113', 'IMAGE', 'https://cdn.chotot.com/6tjFQ8a2bxuzYel3d7CP4iAj06H5TDu9Cw9P9k5khEo/preset:view/plain/6281bc682c8ad3c44fa0d103a749cadd-2996121211377534436.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('47281d81-d2d3-480b-9588-153001833b37', '1480cfe4-3536-410a-8b64-0a4ca18f9113', 'IMAGE', 'https://cdn.chotot.com/dkNQ1wY62VqKqwd-P078NvATx0hzMxXKdnSq_t9zjVs/preset:view/plain/3d2abfef6e6fb8683d093c03630d038c-2996121210993350737.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c8fa52a2-b369-49a7-9785-98bf539279dd', '1480cfe4-3536-410a-8b64-0a4ca18f9113', 'IMAGE', 'https://cdn.chotot.com/vMuQL0U5vw6oOh6Y9VLazM_mR0z4IVV48KliQ75C3_I/preset:view/plain/c25b094285f48f0fca9e759051862d65-2996121209970154391.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e3ae415d-bfc3-4003-9399-8957b32c643c', '1480cfe4-3536-410a-8b64-0a4ca18f9113', 'IMAGE', 'https://cdn.chotot.com/ahTHnQQebDDKaifIbXQ3BrZxpLNEmsyOy53S3sh5q40/preset:view/plain/de731fb04eacdf6959b69ff6217446eb-2996121279175575012.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('841ba26b-2c0e-490c-95ac-82f3a7c92ac5', 'P_126535489', 'APARTMENT', 'prosper  cần bán dt65m2 giá 2.9 tỷ', 'Cần bán căn hộ prosper
2 phòng ngủ, 2 vệ sinh
dt65m2 giá 2.9 tỷ
vui lòng liên hệ!
#prosperplaza
#canhoquan12
#canhophanvanhon', 'AVAILABLE', 'Quận 12, Tp Hồ Chí Minh', 65, 2900000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9389e7c2-4aea-4530-9c73-d5f27d021dbd', '841ba26b-2c0e-490c-95ac-82f3a7c92ac5', 'IMAGE', 'https://cdn.chotot.com/VurPOVnuIqH-FrR7RQoRkLEyB4W84M7SOMzzn9LMlbk/preset:view/plain/2cb0dd272b144270009414b1191157b9-2941345271536098250.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d87c7314-7417-4861-8317-e821de3fefb3', '841ba26b-2c0e-490c-95ac-82f3a7c92ac5', 'IMAGE', 'https://cdn.chotot.com/fqSbNNAw-XSJmuznk-cqTo9I61BUMx5xNTkYLfxyRXE/preset:view/plain/0acc4df649804be41b13d939ddf5c5a3-2941345271475678591.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('261140dd-ea82-4951-b38e-d871123a5230', '841ba26b-2c0e-490c-95ac-82f3a7c92ac5', 'IMAGE', 'https://cdn.chotot.com/5fSZH8ZPACDwLGhXjj0tzGDAksmLnsMO3fkht6JJENc/preset:view/plain/f74bbc8d2a4db8bb5f3761416a7d529a-2941345271439059852.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('226e279c-61fd-4305-a6e8-0a82d0fefefb', '841ba26b-2c0e-490c-95ac-82f3a7c92ac5', 'IMAGE', 'https://cdn.chotot.com/GSrrOfikjoG9wKYHyhqwJB9OdjfnKg0RW20U0RFzPGA/preset:view/plain/5b9373cef77b1ed854e3e384c866fe4b-2941345271685808315.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('eefe1145-ff79-4ad4-b6a2-8065bd7c3e48', 'P_133940456', 'APARTMENT', 'Cần chuyển nhượng lại căn 2pn đã tt 95% chờ sổ', 'Người quen gửi bán căn hộ ở chung cư vĩnh lộc a
dt 69m2, 2pn, 2wc, đã thanh toán 95% chờ sổ
Nhà hoàn thiện, nhà trống chưa có nội thất', 'UNDER_OFFER', 'Huyện Bình Chánh, Tp Hồ Chí Minh', 69, 1900000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('453b628b-3930-4669-94e8-e9796a070027', 'eefe1145-ff79-4ad4-b6a2-8065bd7c3e48', 'IMAGE', 'https://cdn.chotot.com/OkK90W7rYHcCX7Yp7otAMpwDcs9Eb0nHFRxzDr5JTxM/preset:view/plain/6a3f4d4786613aa19854ce4618e5efd7-2996121055515196141.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a4baf55e-668a-456c-b89d-b6bb5a97ece3', 'eefe1145-ff79-4ad4-b6a2-8065bd7c3e48', 'IMAGE', 'https://cdn.chotot.com/8hp1FM-7ZhJFtjeRgodrwMBHXHT1AJUFkI26yMKjlz8/preset:view/plain/1ff228852e522715d5e870388a697cfa-2996121055237720441.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2338bfd5-0aeb-48bb-bf7d-c7e37493b387', 'eefe1145-ff79-4ad4-b6a2-8065bd7c3e48', 'IMAGE', 'https://cdn.chotot.com/BKVZ3pGn7yg-C8BUOXJptBRd157L2DDIIQnw8ZEGpBE/preset:view/plain/6e4165ebd4a1fadea724355094a31d9e-2996121055594390564.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('abe3f243-1287-4696-bf39-df7812ea01c7', 'eefe1145-ff79-4ad4-b6a2-8065bd7c3e48', 'IMAGE', 'https://cdn.chotot.com/L2CBLjqSR2xLhErrNa4StzmCc1l2k35vxD5kSq0DqUs/preset:view/plain/45159735970e0942ea2631830967b873-2996121055396218340.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('58ca7710-4ec3-43fa-9a87-596d07f5ea69', 'P_133940454', 'APARTMENT', 'CHỈ 900 TRIỆU – CÓ NGAY C.H LÊ THÀNH AN LẠC 37M2,MUA Ở HOẶC CHO THUÊ!', 'Cần nhượng lại căn hộ chung cư Lê Thành An Lạc (Đường Lê Tấn Bê, P. An Lạc, Q. Bình Tân) dạng hợp đồng thuê dài hạn 49 năm. Giải pháp an cư hoàn hảo cho gia đình trẻ hoặc nhà đầu tư mua cho thuê dòng tiền ổn định!
Diện tích: 37m2 – Thiết kế tối ưu, vuông vức, căn hộ thoáng mát.
​Công năng: 1 Phòng ngủ, 1 WC, Phòng khách, Bếp, Ban công / Lô gia riêng biệt.
​Hình thức: Hợp đồng thuê 49 năm (Pháp lý rõ ràng, thủ tục sang tên nhanh chóng).
​Tình trạng: Nhà sạch đẹp, dọn vào ở ngay không cần sửa chữa nhiều.
​Tiện ích nội khu: Công viên, siêu thị mini, bảo vệ 24/7, hầm xe rộng rãi, phí quản lý cực kỳ bình dân.
Vị trí thuận tiện:Đại lộ Võ Văn Kiệt, Kinh Dương Vương, Bến xe Miền Tây, di chuyển vào các quận trung tâm Q.5, Q.6, Q.11 chỉ 10-15 phút.
', 'AVAILABLE', 'Quận Bình Tân, Tp Hồ Chí Minh', 37, 900000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('987230f9-3cef-46b6-82e6-601c6b390407', '58ca7710-4ec3-43fa-9a87-596d07f5ea69', 'IMAGE', 'https://cdn.chotot.com/cHE5Z2KCNAkTMS6xfQlpiWkHEUrtdAZd9e9YphMn3FM/preset:view/plain/e10ed93feffe410ab9bd70aa8beabe6f-2996120870102344740.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d277d22b-93ec-4861-ab76-627d0f6d90ba', '58ca7710-4ec3-43fa-9a87-596d07f5ea69', 'IMAGE', 'https://cdn.chotot.com/Z30qkuoSsfZQH2LKfnvZFzll__3zZrY5d1LNRkxJAeA/preset:view/plain/97d1a6e80522fc71fecbc40027249647-2996120891136690553.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('56676387-4b64-4251-a621-b80206ba90e0', '58ca7710-4ec3-43fa-9a87-596d07f5ea69', 'IMAGE', 'https://cdn.chotot.com/5O6p0k5gNE3Eu7zYp4hax2lQAo0Df3r1yyKJlntkW5Q/preset:view/plain/41643449fd8d8b81e2065fd3ff9a3d42-2996120891915421156.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('623f965b-2925-4308-8201-b98f0eb11fea', 'P_131200101', 'APARTMENT', 'Cho thuê căn hộ an phú 2pn nội thất cư bản', 'Cho thuê căn hộ an phú 2pn nội thất cư bản', 'UNDER_OFFER', 'Quận 6, Tp Hồ Chí Minh', 100, 10000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('84c3fd3d-672a-4bc0-bce6-38aa03bbc062', '623f965b-2925-4308-8201-b98f0eb11fea', 'IMAGE', 'https://cdn.chotot.com/kJx5mshKhV1FUi5_1YUnMotCwHxAX3ogwSHxe6SK1ZU/preset:view/plain/d30c7e84dfcbb3cf55c4dba079b55a49-2993515474458632202.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8e31ed5e-3c04-4baf-9910-537482d43ee6', '623f965b-2925-4308-8201-b98f0eb11fea', 'IMAGE', 'https://cdn.chotot.com/1wGE3QD8MTMtCEcRpolHPD9XqC62oP5Y7vr9gC7Z8bI/preset:view/plain/e7c95b805d973d0b3e793c17a4171d30-2993515446398195718.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b13182f9-2fa0-4d78-8d08-ce18f62f9d94', '623f965b-2925-4308-8201-b98f0eb11fea', 'IMAGE', 'https://cdn.chotot.com/hIUVPIYnD2Q7KzWuXIAk3PPDp73nOulvBsXcG8YbvWE/preset:view/plain/f494e8b60bfb28657bcbdae62343a5f7-2993515465216344705.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b35a15f5-e5c0-44ff-be70-e5f6f498ac2f', '623f965b-2925-4308-8201-b98f0eb11fea', 'IMAGE', 'https://cdn.chotot.com/Z9gQSuDDho-QzDRFhP8KhaSuJG-3l316DfuKAm1AsXY/preset:view/plain/506039ddce28b4ef51691925c2a56c1b-2993515486693817361.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c3ac1e42-af72-441b-af3b-9312fa92583d', '623f965b-2925-4308-8201-b98f0eb11fea', 'IMAGE', 'https://cdn.chotot.com/a1tavXthmz0RN5X-2tsH9WzjIgPOFqOyQLIPqxR39tU/preset:view/plain/4d9342a7dca6f3e408e6ce9a68aeaa5d-2993515460210727751.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6aed2e8f-846b-4242-9a5b-d78fbc4ef584', '623f965b-2925-4308-8201-b98f0eb11fea', 'IMAGE', 'https://cdn.chotot.com/64PjR2H2lBi9iem14pJhEOqdPE69ibDRs965AfBXuSg/preset:view/plain/f3004b22f1401196c00f039d1a254880-2993515494470392647.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('9ee2ff46-28e7-48b3-ada0-e78565f4b479', 'P_132478154', 'APARTMENT', 'Giá cực tốt–CHDV sang trọng,full nội thất cao cấp,gần Bến Thành', 'Dự án: 
Thông tin chi tiết: ⭐ CHDV NGAY NGUYỄN CÔNG TRỨ – PHƯỜNG NGUYỄN THÁI BÌNH ⭐
Căn hộ thiết kế hiện đại, không gian sang trọng và thoáng mát với ban công riêng đón ánh sáng tự nhiên.
⭐ Vị trí trung tâm thuận tiện di chuyển sang Q1, Q4, Bình Thạnh
⭐ Full nội thất cao cấp: giường, nệm, tủ đồ, máy lạnh, máy giặt…
⭐ Ban công rộng thoáng, view đẹp, phù hợp thư giãn sau ngày dài
⭐ Khu vực an ninh, giờ giấc tự do
⭐ Chỉ xách vali vào ở ngay
⭐ Gần chợ Bến Thành, phố đi bộ Nguyễn Huệ, Takashimaya và nhiều tiện ích xung quanh.', 'AVAILABLE', 'Quận 1, Tp Hồ Chí Minh', 40, 8000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('65dda64a-6515-4882-925d-2de2acdb8404', '9ee2ff46-28e7-48b3-ada0-e78565f4b479', 'IMAGE', 'https://cdn.chotot.com/X5IYC6vH9mI4ypD0ij6BqmxawxbacmVnNauKxrTmgNc/preset:view/plain/cf21cc5fab90f5b6078526979697a26a-2984967071355172049.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6742ff6a-c464-4cd2-a016-d44debf80c0a', '9ee2ff46-28e7-48b3-ada0-e78565f4b479', 'IMAGE', 'https://cdn.chotot.com/a-caJyitjGfH_0-XXYdvUk4iO-FO7zqQlEZ07tf43Pc/preset:view/plain/1dc899e20f4b596be7cf72ae574dd1c6-2984967071606072369.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('33bf06e1-6186-4749-a946-69be1c797d01', '9ee2ff46-28e7-48b3-ada0-e78565f4b479', 'IMAGE', 'https://cdn.chotot.com/OOpWNXCKxNTA4BZxl45xfzTKNipDuWGUatzv0AM_pGw/preset:view/plain/17ae72f5a00637edf6cf017fc4881788-2984967071486588321.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('02517d9f-0a59-4a38-a099-63dd63339d83', '9ee2ff46-28e7-48b3-ada0-e78565f4b479', 'IMAGE', 'https://cdn.chotot.com/sy0CuNqznfXlrp-7CFuHakxy4vaVPzc5FoIzIa7l-gc/preset:view/plain/d0178c0081a3a9ad217a55327cbc095c-2984967071569352139.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d85266dc-adcd-4202-ba71-0e7dc4a93c81', '9ee2ff46-28e7-48b3-ada0-e78565f4b479', 'IMAGE', 'https://cdn.chotot.com/IQktrBVysFllf9Ajk-A2ERkD2xv0altJRZF2V4yHRBo/preset:view/plain/92df87ad069a04bfee89262e01608e26-2984967071618677331.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4759600f-fb54-4b1c-b8dd-b6a823f1554f', '9ee2ff46-28e7-48b3-ada0-e78565f4b479', 'IMAGE', 'https://cdn.chotot.com/OxFqH6VH8shBDbB8hfGoxMGmdWy0sBXWHlqN5F4dJLw/preset:view/plain/4ed4ef8529545f4cf88dae689b038c30-2984967071572415189.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4f74849a-20e7-473c-a2ae-3db636c378c2', '9ee2ff46-28e7-48b3-ada0-e78565f4b479', 'IMAGE', 'https://cdn.chotot.com/wUwSiNhen7o8AsIRscs7-xL1zU2Tp7zM3duPmExVKSY/preset:view/plain/03e9ae1dfdc392ce0e45116d178602b0-2984967071514440169.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('078d1296-1184-4fc8-99f1-1b2781a26b37', 'P_114780020', 'APARTMENT', '4.1TỶ 2PN, 3.2TỶ 1PN, LAVITA CHARM TRỤC CĂN VIEW METRO THOÁNG MÁT', 'LAVITA CHARM 2PN

Bán căn 2 phòng Lavita Charm.
Diện tích: 67 m², 2PN 2WC.
Giá 4.1tỷ, nhà có nội thất như hình ạ



Bán căn 1 phòng Lavita Charm.
Diện tích: 53 m², 1PN 1WC.
Giá 3.2tỷ, nhà có nội thất như hình ạ', 'AVAILABLE', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 68, 4099999999, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ccdfc682-a5f7-46f6-826b-b29ead1eed13', '078d1296-1184-4fc8-99f1-1b2781a26b37', 'IMAGE', 'https://cdn.chotot.com/bJXUoRxIQnyMbxV6i87CGih410h8pbEnko1SNFcustU/preset:view/plain/84af6371970ae4e677f70dc544eabe8a-2870299139136086694.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c04999c0-a0e1-4b3b-a368-f462eb9176eb', '078d1296-1184-4fc8-99f1-1b2781a26b37', 'IMAGE', 'https://cdn.chotot.com/Y_oD8LoXCLfzp6vZu1wBbLR1DgYhT7dpoNzOYqeQPdM/preset:view/plain/a1d546d3de28dcd1d2767710589263e8-2870299142268658864.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('857a3306-0cd3-4768-a9b7-13abe7317ea7', '078d1296-1184-4fc8-99f1-1b2781a26b37', 'IMAGE', 'https://cdn.chotot.com/1fHa6-mtcUpUjqMhW4j1Fa_9Ug9pe-uXTz0RzTLkMfE/preset:view/plain/4f5870dee9d8bb5a285179ab0c69cc48-2870299147759837862.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('81ad7426-f506-4f4c-8f2b-2f90d04a169d', '078d1296-1184-4fc8-99f1-1b2781a26b37', 'IMAGE', 'https://cdn.chotot.com/pjrZz2fZ3Qi2ieq_mDbJrIbqfmKOnvSvF71iWGp2Hlo/preset:view/plain/54458c9d1851d4b7508a5e0ad7ae3db0-2870299166597515408.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('51007a22-7748-4470-983b-ad2a10620086', '078d1296-1184-4fc8-99f1-1b2781a26b37', 'IMAGE', 'https://cdn.chotot.com/nAr2f1pnU_IDKgo0jn0YqX7JCTVQbR2ChBtcUEmXLXA/preset:view/plain/92c42ba083f3bc9de3671794b680f92a-2870299166718550694.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('3362ad2b-4479-48f1-9bf8-883299267e7a', 'P_133803849', 'APARTMENT', 'Cho Thuê Căn Hộ Ban Công Full NT Rộng 27m2 Gần ĐH Kinh Tế UeH Q10', 'Dự án: 
Thông tin chi tiết: vị trí : Ngay Thành Thái, Sư Vạn Hạnh, Tô Hiến Thành, 3 Tháng 2 

Full Nội Thất 
Hẻm Oto 
Khoá Vân Tay
Giờ Giấc Tự do 

call/zalo hoặc ib cho Khang', 'SOLD', 'Quận 10, Tp Hồ Chí Minh', 27, 6000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bf0b1afd-6665-406e-85ff-e5d44392b9ba', '3362ad2b-4479-48f1-9bf8-883299267e7a', 'IMAGE', 'https://cdn.chotot.com/7y9w4hGvFjxMav5PZQODIY1EINPepHcH0eyR7itvjTs/preset:view/plain/fb0870b3960b2ff22a4da12259d6b27d-2995975334854129236.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1bac0769-c01a-4503-8522-7b01df2097f9', '3362ad2b-4479-48f1-9bf8-883299267e7a', 'IMAGE', 'https://cdn.chotot.com/XulriKqsRP8MyhaQRTV_YFo_MeOHxioD-8v3DXwiHFw/preset:view/plain/0db9634762e2b94adab6c205be41240c-2995975334745213524.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c0983de9-b2ad-4c90-9409-54b4db751a57', '3362ad2b-4479-48f1-9bf8-883299267e7a', 'IMAGE', 'https://cdn.chotot.com/NAGUJep3NT3azaI34oxPACtgYaxbkfb9_SsYQbPwBKw/preset:view/plain/271278ffde4f2cbf9e8d2632e4d1fb33-2995975334779505017.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8b1aca16-dd83-4f8b-b848-f4b5ab9447a4', '3362ad2b-4479-48f1-9bf8-883299267e7a', 'IMAGE', 'https://cdn.chotot.com/ukj1MoZgX9cx3LSSvdVYc5VXIUkTxp9xVST3un4CVx0/preset:view/plain/b1d0167bd908e1b1dc5a9532df78bf37-2995975334838869622.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f807c5b5-d9df-4b9b-9aa1-fc39da73dd54', '3362ad2b-4479-48f1-9bf8-883299267e7a', 'IMAGE', 'https://cdn.chotot.com/BG14H6pY9wu9zBEkc0Lw1hnc9e8X9WR-jAWOZDzH6Ng/preset:view/plain/a4b17955ee11ec6a1d37d5abfbf620c9-2995975334971692131.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('de2bf98d-469f-4712-b6af-71dada02c64c', '3362ad2b-4479-48f1-9bf8-883299267e7a', 'IMAGE', 'https://cdn.chotot.com/lbKFeT3ojBHKP8_GYQyt9oVKZgJ5o3LXxBahoB0_fF4/preset:view/plain/1e71648d500e900db9886bdae588b624-2995975334946466537.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('26b528e8-2d7f-4c83-9c1c-42e809bb9d5f', '3362ad2b-4479-48f1-9bf8-883299267e7a', 'IMAGE', 'https://cdn.chotot.com/qsnG7pHRoqvdtIpGIlVv4xkPpTm4W9VHHp8jT6KQfZY/preset:view/plain/bc2667b53ee4a1b00e2680eaa571b92d-2995975335312516712.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('dd8d6ddd-ee89-4d0d-86bc-49eeee0c473c', 'P_133529553', 'APARTMENT', 'Giảm sốc bán 2PN 89m2, Vinhomes Central Park, view sông', 'Dự án: 
Thông tin chi tiết: 🔥Giá sốc căn 2PN P7 28 12, chỉ bán trong tuần này

💲Giá chốt 10 tỷ bao thuế phí. Giá áp dụng bán trong tuần này. Tuần sau chủ có kế hoạch khác

👉2PN 89m2 nhà hướng nam, view sông mát cả ngày

👉Full nội thất, sổ sẵn

☎️*** Huyền Cty Ruby homes SG để chốt nóng', 'AVAILABLE', 'Quận Bình Thạnh, Tp Hồ Chí Minh', 89, 10000000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('eff3253f-2ab8-4f87-a83e-b2f8daf68a72', 'dd8d6ddd-ee89-4d0d-86bc-49eeee0c473c', 'IMAGE', 'https://cdn.chotot.com/ZGjbqkENrjp_lJq0PFSYq7lAUeJQ2zOIXGLMjDG5dcw/preset:view/plain/19e5fa7c740210c3f8b3bcaceaab2cdb-2992969945200720771.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3eed58d2-2c5f-41c9-a5f7-bbaca0e230f7', 'dd8d6ddd-ee89-4d0d-86bc-49eeee0c473c', 'IMAGE', 'https://cdn.chotot.com/cf5qZOOA_j58ZaavBVifw_Y-b5iZeBRrY61kSzkMRBI/preset:view/plain/7339659c5f32340075ce26068468acb5-2992969944751076877.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b2a09c40-b577-4283-b151-05643e01dbec', 'dd8d6ddd-ee89-4d0d-86bc-49eeee0c473c', 'IMAGE', 'https://cdn.chotot.com/H7olr5Wpapb-jJw3EL4Bo1cjPVTu9h180SU_AjBWAcY/preset:view/plain/3305a8ca92b2e6cfa28e92ab8ffb5ea5-2992969945160365363.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('34ef81a9-2e65-4611-bd59-8c549db2c8a3', 'dd8d6ddd-ee89-4d0d-86bc-49eeee0c473c', 'IMAGE', 'https://cdn.chotot.com/TyUapsXJNbXu4bOIrZjnufMstF25OUUF9BsCczc5HWQ/preset:view/plain/004fd7f5699b67054482fe9fcd0147b3-2992969944890949687.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3ca3c715-6ca4-4b54-87b1-08dc4a1b4b77', 'dd8d6ddd-ee89-4d0d-86bc-49eeee0c473c', 'IMAGE', 'https://cdn.chotot.com/0Y9s3XK0NPawV7WSX8rZKjYMbIh64KNeAbRWMySg2rI/preset:view/plain/a37e3fa0e4212c81d1b3cd4bc54b0451-2992969944994572575.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('14617ef6-ffd8-4e8e-a266-d4ad2c50763e', 'dd8d6ddd-ee89-4d0d-86bc-49eeee0c473c', 'IMAGE', 'https://cdn.chotot.com/80dz0nbY__v9c8G65CBybtPXgY_FZI3WgCh3y5T_Ugg/preset:view/plain/91aafe9e7b8dc36ccb45475d50334b34-2992969945103960219.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d6882234-f076-44eb-9244-1e054fb4a96d', 'dd8d6ddd-ee89-4d0d-86bc-49eeee0c473c', 'IMAGE', 'https://cdn.chotot.com/9fg7E3OI8dBjT39j8j2qvSLuMmCPsrugfvHl705CbH0/preset:view/plain/fca38a58718f244d4cfce108166851b3-2992969944968464022.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('171f32cc-1a03-4c94-b374-9a5603d581ca', 'dd8d6ddd-ee89-4d0d-86bc-49eeee0c473c', 'IMAGE', 'https://cdn.chotot.com/OOAP9dv5Evnau22cziIZdWPqIxFvvj0duJk7w3X8P1k/preset:view/plain/317de9ad4d9bb9a0c812f55f8a61de76-2992969945016726295.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a04cca2f-e1fa-4bdd-8068-18a548424f1b', 'dd8d6ddd-ee89-4d0d-86bc-49eeee0c473c', 'IMAGE', 'https://cdn.chotot.com/SKTGDa9yAGch-L9IHCTWJzVR4Eo4p9azpmdd8SvBhdI/preset:view/plain/5c63942c1f6c091cde43fab929b02612-2992969944895726430.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0f239c28-3777-4d42-955a-4c083bfa99d8', 'dd8d6ddd-ee89-4d0d-86bc-49eeee0c473c', 'IMAGE', 'https://cdn.chotot.com/utLP1b5OxQNDn60xcz9KtzgiJ9ydQVQ7VlrKkdpMX84/preset:view/plain/bb00dda213d7979a19bdfa00fbe0362c-2992969945208690673.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('42abc595-1cb3-499f-9d9f-4dec29ff69b3', 'P_131373172', 'APARTMENT', 'TRỐNG Căn hộ ban công cao cấp, sang trọng, hiện đại, gần ga Metro', 'Dự án: 
Thông tin chi tiết: 🔥 SIÊU PHẨM BAN CÔNG HIỆN ĐẠI – SANG TRỌNG NGAY TRUNG TÂM Q1 🔥
📍 Nguyễn Thái Bình, Quận 1
✨ Căn hộ ban công riêng – không gian thoáng sáng, cực chill
✨ Thiết kế hiện đại, sang trọng, tối ưu từng góc sống
✨ Full nội thất cao cấp, chỉ cần xách vali vào ở
✨ Vị trí đắc địa Quận 1, gần
• Chợ Bến Thành – ăn uống, mua sắm sầm uất
• Phố đi bộ Nguyễn Huệ – vui chơi, check-in
• Takashimaya Saigon Centre – trung tâm thương mại cao cấp
• Bitexco Financial Tower – biểu tượng tài chính, view cực đẹp
• Bến Bạch Đằng – dạo mát, ngắm sông
✨ Khu an ninh, yên tĩnh, phù hợp ở lâu dài hoặc chuyên gia
✨ Giá cực tốt – ưu tiên khách thiện chí chốt nhanh
📞 Liên hệ xem phòng: ***', 'SOLD', 'Quận 1, Tp Hồ Chí Minh', 40, 9000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('06788532-9840-4a94-abdd-5ac4cf7a7928', '42abc595-1cb3-499f-9d9f-4dec29ff69b3', 'IMAGE', 'https://cdn.chotot.com/abVuG-aAtTIiQKgqs0a-3CVohN8WOTXC4PLgRjN46r0/preset:view/plain/67b41001f1bfc412e5cbcd437ec4e6c6-2976687217449121644.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9b6cabc5-5180-4e21-a8cd-b7eea3a7bdc1', '42abc595-1cb3-499f-9d9f-4dec29ff69b3', 'IMAGE', 'https://cdn.chotot.com/cHvjgAemRPsu43QFRsRxOg4FTlT8MnDscFkSEjtFI70/preset:view/plain/3136b8e2184ed62f07981e2ffc9ce7cf-2976687216802862504.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('73ac14a0-3940-4e88-b8bc-287b5bce766a', '42abc595-1cb3-499f-9d9f-4dec29ff69b3', 'IMAGE', 'https://cdn.chotot.com/Ci_iH6UYVx62F1dDMmaYDbAJCJTQUikE5beN7Wfg8Gw/preset:view/plain/d0879c8f9a2127619c598e0cbef2d0f3-2976687218036389740.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('09d673ae-2ed1-4502-8816-3a7fb8e8f7d8', '42abc595-1cb3-499f-9d9f-4dec29ff69b3', 'IMAGE', 'https://cdn.chotot.com/P6td8TZxPYgP-BEd2YqtXCIB0gRdsXR1CDlqkqPlFJ4/preset:view/plain/24996147b629c802ba75817db5d43963-2976687219277969260.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('069451e9-25ca-4470-9e6b-674863257fe4', '42abc595-1cb3-499f-9d9f-4dec29ff69b3', 'IMAGE', 'https://cdn.chotot.com/yIz6yvAZ2At4vD1HgFTv9BF_X1BRwB0X3KyYKRbMjYs/preset:view/plain/14c69bb93b9e829ca945a35c22a292fb-2976687219630356332.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('98639151-dc75-4e1d-a023-8298d805e96d', '42abc595-1cb3-499f-9d9f-4dec29ff69b3', 'IMAGE', 'https://cdn.chotot.com/mzCciJ62Z_wGqM57ibAvV0erqZYkPtXfGeFmUpUAs1k/preset:view/plain/25b45b49c1408413edef0d693a0c57bf-2976687219723646217.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0d809f29-b280-412e-a4fd-6a68d96c9979', '42abc595-1cb3-499f-9d9f-4dec29ff69b3', 'IMAGE', 'https://cdn.chotot.com/hVwJNq8MA_w4WzSObMaiVbGbsEFJoo00cmEX8NUEDGA/preset:view/plain/01e48b3250256259c0a4e987de3ce739-2976687218413540776.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a2925467-138f-41a2-b326-3564fcdf98aa', '42abc595-1cb3-499f-9d9f-4dec29ff69b3', 'IMAGE', 'https://cdn.chotot.com/kE79W2PeKO6MKSDyyUmPIGOQGcGCdX2xMsWDD4HzkJU/preset:view/plain/279aeff784d714bb1ecec2b034b0efbb-2976687219182193391.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('775b6a2f-42cb-4f01-905c-f6dfdd2dea18', '42abc595-1cb3-499f-9d9f-4dec29ff69b3', 'IMAGE', 'https://cdn.chotot.com/dV_vQrHsApzKiL83YMCDpDn6Wn3VgG3UZKEJ4ktU9lI/preset:view/plain/0073c6f2081a21769e216607c5e7078a-2976687219857929481.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('3408705d-47cf-410f-85b8-c479a6244353', 'P_130705468', 'APARTMENT', 'Bán căn hộ Mizuki Park | 58m2 2PN 1WC | Sổ Hồng Sẵn | Nội Thất Đẹp', 'Thông tin căn hộ các sản phẩm.
- Diện tích: 58m² - View đông bắc siêu tốt
- Thiết kế: 2PN, 1WC.
- Giá về tay chủ mới: 3,7 tỷ | Giao nhà hoàn thiện.
- Giá về tay chủ mới: 3,9 tỷ | Giao nhà đầy đủ nội thất đẹp.
Sẵn sổ hồng chính chủ.
------------------------------
Căn hộ mới 95 -98%.
Tiện ích khu căn hộ đầy đủ phục vụ cư dân.
Hỗ trợ tư vấn vay vốn - thủ tục sang tên nhanh nhất.
Liên hệ xem nhà ngay hôm nay', 'AVAILABLE', 'Huyện Bình Chánh, Tp Hồ Chí Minh', 58, 3700000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a8d645cd-f079-4a70-9f50-1b6ef7fbad37', '3408705d-47cf-410f-85b8-c479a6244353', 'IMAGE', 'https://cdn.chotot.com/02lcy6PWLMEmqJvieV5MvaNKy4M_ZKIyu7zOb8o12lE/preset:view/plain/0e6455b600b188d44eeda980b9461717-2970324139967577594.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6e68ad81-1f3a-4cfd-a100-1d046db988ea', '3408705d-47cf-410f-85b8-c479a6244353', 'IMAGE', 'https://cdn.chotot.com/RV9TIEamnz3a9ZH74FFvB6VXs67w7TTk1hmgXl-Z8G4/preset:view/plain/f4396db4d44ba5b5c0e8bbddd6607d3c-2970324139847095976.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9afc4737-0e0a-4ab8-a59a-12ca11e5804b', '3408705d-47cf-410f-85b8-c479a6244353', 'IMAGE', 'https://cdn.chotot.com/t-aOeSI7e5k9BInAwnTVNTJindow5Gox7yUy3wpbErk/preset:view/plain/8e141d0e8720ab6f7a854db8e5cfec79-2970323946634934541.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('21e3338f-709d-444b-8426-01e3635263f7', '3408705d-47cf-410f-85b8-c479a6244353', 'IMAGE', 'https://cdn.chotot.com/XTmOfKj2x8EIp82w_8sQXuUlZuNBqQ-rJlj31N5IHuw/preset:view/plain/e26b2a2dae7db275a3a6cafee7c2113d-2970323946541368757.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cae35602-bfa6-4e1c-bcc6-dd9dce160d00', '3408705d-47cf-410f-85b8-c479a6244353', 'IMAGE', 'https://cdn.chotot.com/OEYqzR5DtZKjhQi3A37yElJLa6kPD6f_KNI5hCuo5mo/preset:view/plain/6d41bd94da9f5a204ebd59d2daedf827-2970323946587985576.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d0dfdc31-8aee-4944-a7d0-afc539d9ae49', '3408705d-47cf-410f-85b8-c479a6244353', 'IMAGE', 'https://cdn.chotot.com/3KhCx92MlnUJnP7UHT23bcac4k6Y4JUIAPwUNy0pBgM/preset:view/plain/6a5ca52d2718a1d4fd43fa7d458eaf66-2970323946594438278.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('09e88003-cf56-4f0b-930b-714398a094ec', '3408705d-47cf-410f-85b8-c479a6244353', 'IMAGE', 'https://cdn.chotot.com/j3fZS_LFQxkCiLmGMvaCjzt6D_VZh7QVMU_2em_DEEw/preset:view/plain/604c0def9b335741994190d13d9bc8e4-2970323946759978490.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bb40c995-f4ce-44fb-ab71-b946dd02f69e', '3408705d-47cf-410f-85b8-c479a6244353', 'IMAGE', 'https://cdn.chotot.com/d0IGi0LenWaX3OKRxThMrYTK3GYzIbHrGUHXxshzoGY/preset:view/plain/9a028040c381b32a494ce478937c0b52-2970323947041236045.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d6f2d7a9-0ec6-4abe-bfb5-2aa273c9ece0', '3408705d-47cf-410f-85b8-c479a6244353', 'IMAGE', 'https://cdn.chotot.com/8hXJ0jLD_7Nk-J7YryGcxjF3uBI3saRxtx5wrGVyI0w/preset:view/plain/94903d682a799753890d3ff7d049c97a-2970323946765201050.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0574adbe-c9bd-4963-8392-dcc9d21b170d', '3408705d-47cf-410f-85b8-c479a6244353', 'IMAGE', 'https://cdn.chotot.com/j8aFWCeO_0rbbnJ2_JlOoj68p50mvNkaGP21c05jPfI/preset:view/plain/b30331644c2ab26b6231aad1898dc1af-2970323946707436172.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('22207623-c61f-41d6-8f6c-a58f7dd02525', '3408705d-47cf-410f-85b8-c479a6244353', 'IMAGE', 'https://cdn.chotot.com/VI8e_OJHoyuLEhrG9WWLOIVRzkVPSyCqKpMfxdh14J8/preset:view/plain/725197b1565b60289dd2d1138f7e6bd7-2970323946735233516.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('864b108b-a887-4f11-8fc1-22913a1a0a13', 'P_133505618', 'APARTMENT', 'CHO THUÊ CHDV GẦN LOTTE MART', 'Chi tiết: CHDV Duplex Quận 7 gần Lotte Mart, Cresent Mall, PMH, TDTU, RMIT, UFM.

Tiện ích: 
- Full nội thất, diện tích rộng, thiết kế tone sáng tạo cảm giác thoáng mát, dễ chịu
- Khu dân cư an ninh, giờ giấc tự do
- Gần cửa hàng tiện lợi, bách hóa xanh, phòng tập gym, khu vui chơi, ăn uống

ĐỒNG HÀNH CÙNG BẠN TRONG QUÁ TRÌNH "Tìm - Thuê - Ở"
Liên hệ: ***

#thuephonggiare #thuetro #thuephongquan7 #canhodichvu #canhocaocap #canhoquan7 #canhoduplex #phongtroquan7 #thuecanhoquan7 #canhogiare #canhohcm #canhogiarehcm #thuetro #phongtrosinhvien #canhosinhvien #phongtrocaocap #phongtromoixay #canhomoixay #trosinhvienhcm #phongtrotphcm #phongtrodep #canhodep #canhomini #canho #canhominigiare #phongtrosinhvien #phongtrohcm', 'UNDER_OFFER', 'Quận 7, Tp Hồ Chí Minh', 35, 4700000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('aeed9e47-aeeb-498c-9747-8d847ceae172', '864b108b-a887-4f11-8fc1-22913a1a0a13', 'IMAGE', 'https://cdn.chotot.com/qWUoovfMrFHiRH-XdUfyCDka2jeByWbL6RcGTfiEe-8/preset:view/plain/a2657dd2f17669725f12c84e114eca6d-2992795322509130290.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('086e870b-15b9-4986-bb21-9accfc014039', '864b108b-a887-4f11-8fc1-22913a1a0a13', 'IMAGE', 'https://cdn.chotot.com/UNbTKKxsLOIcot5ReeYIvvrPyeo1DZnjf0LjupKgkXw/preset:view/plain/17aaa8dafd0777d14b8fd30cd0c6c3c9-2992795322664661939.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e9790c1b-6d92-4019-bc3c-fe792e69ee3d', '864b108b-a887-4f11-8fc1-22913a1a0a13', 'IMAGE', 'https://cdn.chotot.com/KTGD_BsvltujMyqvUK7SeAR2nF5pahmITWFW7jviN3A/preset:view/plain/0b74c24a4a340e053e2d67ad4ef23b34-2992795322650138587.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('13f34b84-c5ae-48a6-a4cc-07e626df240c', '864b108b-a887-4f11-8fc1-22913a1a0a13', 'IMAGE', 'https://cdn.chotot.com/6a0ByT1OCRkhEDxuHQ_r6KgZ4PD-uK1sHWCqGrO4tg8/preset:view/plain/aad494d90b112bbcecdc90cfd6af5b46-2992795322629239021.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('90b53aed-d456-41e0-8220-70d6b13659df', '864b108b-a887-4f11-8fc1-22913a1a0a13', 'IMAGE', 'https://cdn.chotot.com/YgYscFypgqDH2o12d_7O0PpKWyfLcn1epqdWGjX_Exc/preset:view/plain/4f767efa1b2e918a45a5e29a7a13b5a3-2992795322657603626.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7a1b9552-4539-46c2-88e6-25a38f22e5e3', '864b108b-a887-4f11-8fc1-22913a1a0a13', 'IMAGE', 'https://cdn.chotot.com/Im0uXaKnYM16Be6osHPl72i8_yKOu37_BuOgKfrKWlM/preset:view/plain/3a065b133168580e3d0d812982bbc41c-2992795323170147214.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a66ff8c7-74e1-4de6-9411-f98fb0617331', '864b108b-a887-4f11-8fc1-22913a1a0a13', 'IMAGE', 'https://cdn.chotot.com/L0MSxNcwccMUCImQDc0EC-3-N7cP10YpfFaVaWNh6XM/preset:view/plain/1922a40f05a96d28b93314e4701e7e0b-2992795322518590138.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('15016856-1019-48d7-8836-de07f8b18750', 'P_133940403', 'APARTMENT', 'Bán căn hộ Belleza 124m2 . sổ hồng . Giá :5.5 tỷ .', 'Dự án: 
Thông tin chi tiết: 🏡 BÁN CĂN HỘ BELLEZA – QUẬN 7

✨ Diện tích: 124m²
🛏️ 3 phòng ngủ – 2 WC
🛋️ Có nội thất
📜 Sổ hồng riêng
💰 Đang có hợp đồng thuê – Mua có dòng tiền ngay

💵 Giá bán: 5.5 tỷ (còn thương lượng)

📲 Liên hệ ngay : ***', 'UNDER_OFFER', 'Quận 7, Tp Hồ Chí Minh', 124, 5500000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0b0291a4-7743-4213-9e1d-9d61e2a39027', '15016856-1019-48d7-8836-de07f8b18750', 'IMAGE', 'https://cdn.chotot.com/8Aj-ni0xVtRBbsW987JAqgRi3diZSHo7VjupbB4eA5w/preset:view/plain/cd92c686244e3f51072ce669c619dc9e-2996121009552509305.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('609a79d0-c98e-4c4e-9990-650ac2670837', '15016856-1019-48d7-8836-de07f8b18750', 'IMAGE', 'https://cdn.chotot.com/BuDtSr0frlOedlFX9jePdp2tdpzgjqREaQwnVHNCLdI/preset:view/plain/d1b393bc6ddab6eb3ef8594bdaf236bf-2996121009544837869.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3de011e6-23ba-4399-8bcf-8a820ffc71ed', '15016856-1019-48d7-8836-de07f8b18750', 'IMAGE', 'https://cdn.chotot.com/Vd2L_DFpoXewNfSmjvLXO7npynfJnPjiaLRMTE3C3qE/preset:view/plain/d57c8dc9d6139d577630079949e972cb-2996121009593501156.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ed578b85-334d-42e9-88f1-0f93147d8917', '15016856-1019-48d7-8836-de07f8b18750', 'IMAGE', 'https://cdn.chotot.com/JlzaX1mHA6LbhTm2qb1miOzp60_O06dNsCAM1sXEMxs/preset:view/plain/f0326975a3c7df01cef6fbfd3eed0bc5-2996121009758184484.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('36e5fc64-3776-454a-bd69-60ca7b435262', '15016856-1019-48d7-8836-de07f8b18750', 'IMAGE', 'https://cdn.chotot.com/rPd3KG217_nd7gM9okHH6WsUfuOHx9yHmUzv5SD-LOg/preset:view/plain/e323615589e4e71392f518c2dd9e52f9-2996121009699430488.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('bb50cec4-8809-4b06-99f8-5f748544ef95', 'P_133163556', 'APARTMENT', 'Cho Thuê Căn 2PN - Căn Góc - Liền Kề Phú Mỹ Hưng', 'Cho thuê căn hộ 2pn 1wc - KHÔNG ĐƯỢC NUÔI PET
Căn góc view thoáng mát 
Tầng thấp nhưng kg ồn , kg bụi 
Khu dân cư yên tĩnh ,an ninh 
Tiện ích xung quanh đầy đủ : Chợ , Siêu Thị , Cà phê , Quán Ăn , Trường học các cấp , CA phường kế bên 
Cách Phú Mỹ Hưng 5 phút 
Ky hợp đồng tối thiểu 1 năm 
Cọc 1 tháng + 1 tháng tiền nhà 
Bàn giao nhà trống như hình 
Nhà mới 100% ', 'UNDER_OFFER', 'Quận 7, Tp Hồ Chí Minh', 56, 9500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a6913555-035e-4291-9796-9f5f0bba191a', 'bb50cec4-8809-4b06-99f8-5f748544ef95', 'IMAGE', 'https://cdn.chotot.com/el75vZzK6tHM7SroFKXGwNu9tzAWfeXsd1yTF8KqCLU/preset:view/plain/b5829649b6a73fb0f84b7d08d0e8c5ab-2990176190796701447.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('60c67bfc-3f39-4d53-b897-c2996b217f36', 'bb50cec4-8809-4b06-99f8-5f748544ef95', 'IMAGE', 'https://cdn.chotot.com/bdsMmFPyOrjvAJBaQNcqfPc1YvAZdhLgKQGoJAAFOEc/preset:view/plain/df1d1ff312109562f16c1e76de5b17d4-2990176190140606212.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2299924f-455d-4ba5-b291-9bbe43d2b2b8', 'bb50cec4-8809-4b06-99f8-5f748544ef95', 'IMAGE', 'https://cdn.chotot.com/cGWOHuVc3QIdVYQKtThwxUkciLS1EkAUqoz4B350zF4/preset:view/plain/1b16e95b4b8fcd4f98159145343d08a4-2990176190251017352.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('ea301f73-cd89-43d3-9bf7-c1e7f0adb4e9', 'P_133940391', 'APARTMENT', 'Cho thuê Căn hộ 1PN, full nội thất, Centana Thủ Thiêm, Đ. Mai Chí Thọ', 'TRỐNG SẴN, NHẬN Ở ĐƯỢC NGAY. CHO THUÊ CĂN 1PN, TẠI CENTANA THỦ THIÊM, Đ. MAI CHÍ THỌ, P. AN PHÚ, QUẬN 2:
- DT 45m2, 1PN, 1WC
- Full nội thất 
- Nhà sẵn, nhận ở được ngay
- Giá net: 12tr/tháng
Gọi Mr. Hân xem thực tế, chốt căn. ', 'AVAILABLE', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 45, 12000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('023d105c-aae3-48a1-87ff-b360fb1ad953', 'ea301f73-cd89-43d3-9bf7-c1e7f0adb4e9', 'IMAGE', 'https://cdn.chotot.com/JUaCEWftgqA-ZL9_jO1O7ZojY8lpkbL6HjDqaNHc58Y/preset:view/plain/3a962b5a27ef042ae95fc208617f05a9-2996120872547010937.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('345773e5-9d11-4568-ab1e-f47e56fb06b1', 'ea301f73-cd89-43d3-9bf7-c1e7f0adb4e9', 'IMAGE', 'https://cdn.chotot.com/D0c0lWiRspdou7a3liru-KtkeXUTtRa5o-ttBB9IHNc/preset:view/plain/aa47c4a804aff9c7a9de3d88a770a75c-2996120872805647844.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('adec3ed5-340c-4cae-be04-d396fe9fc758', 'ea301f73-cd89-43d3-9bf7-c1e7f0adb4e9', 'IMAGE', 'https://cdn.chotot.com/LpMxENocAvFOSmWHl-gTtrXO8SrPEXLZUR8nmQa1jnY/preset:view/plain/7bde94f4388d6dc11a650c708653a6e3-2996120873611019748.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e6a6b969-9505-40b2-9fe4-ac893adb7cda', 'ea301f73-cd89-43d3-9bf7-c1e7f0adb4e9', 'IMAGE', 'https://cdn.chotot.com/c5ai2u59YsSI5DkAbmL9yfdR-abicwnRDJL8t46umKA/preset:view/plain/7972b7bf73603c88cbeb684e64be36fd-2996120873877283876.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('db3233ab-efb6-4cc9-b65b-0c568df1164b', 'ea301f73-cd89-43d3-9bf7-c1e7f0adb4e9', 'IMAGE', 'https://cdn.chotot.com/YAbbfN8zzx9Tarqz-fFp7r7U5wBhlB8iDhweYfSe6fs/preset:view/plain/542843f1ce09102ddeeca98b3b768821-2996120874879175033.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4e50e41d-c016-4d67-abbc-12483a36bd17', 'ea301f73-cd89-43d3-9bf7-c1e7f0adb4e9', 'IMAGE', 'https://cdn.chotot.com/_5EtIeIDcpADBjAjH3Kb-ARWQnGj-Pl82FQx_qHs3TQ/preset:view/plain/6288d1528582ba1d83a55bbf36877f47-2996120875087480292.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ce495084-7539-40b3-b3cd-906068bc2197', 'ea301f73-cd89-43d3-9bf7-c1e7f0adb4e9', 'IMAGE', 'https://cdn.chotot.com/DfziaLcUguYAlL_zMJTVVoOM33YF7vR4xki2iiXRKV0/preset:view/plain/4e0bb631e0b4ffa3f6b60e6fc08a82aa-2996120875892852196.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b2d6a016-60ed-4b69-bc95-ea59ddd3fae6', 'ea301f73-cd89-43d3-9bf7-c1e7f0adb4e9', 'IMAGE', 'https://cdn.chotot.com/NjNFRUpollzSL3rcTOot-bH6R_IT6vr5OtsuREk_0vo/preset:view/plain/498650f2198fde038cc527a22ec56338-2996120876207019304.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4a8f1189-b5ff-41cd-9a9b-d4ff7731bce2', 'ea301f73-cd89-43d3-9bf7-c1e7f0adb4e9', 'IMAGE', 'https://cdn.chotot.com/psDLSTVDf4AAKlXQI6sSHxi1UhKpkA63FOmJZzW5SEc/preset:view/plain/dce06388c9bb97883dbf37605c343e1e-2996120877219920621.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('fc92ee87-5602-42f3-b201-1968e2857247', 'P_133940390', 'APARTMENT', '🔥 CHO THUÊ CĂN HỘ 1PN+ BAN CÔNG – NGUYỄN HỮU CẢNH, BÌNH THẠNH 🔥', 'Dự án: 
Thông tin chi tiết: 📍 Vị trí: Đường Nguyễn Hữu Cảnh, Bình Thạnh (Ngay sát Q1, Landmark 81, di chuyển 5 phút).
✨ Điểm nổi bật:
 - Phòng ngủ tách biệt : ban công cực rộng, view cao thoáng mát.
 - Full nội thất cao cấp: Sofa, tủ lạnh, máy lạnh, tủ quần áo lớn, bàn trang điểm, giường nệm.
 - Khu bếp riêng biệt: Tủ bếp trên dưới, bồn rửa, máy hút mùi sẵn có.
                  - WC sang xịn: Vách kính tắm đứng,            gạch decor hiện đại.', 'UNDER_OFFER', 'Quận Bình Thạnh, Tp Hồ Chí Minh', 40, 8500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e245d306-1bbc-45db-92fc-43177ce69897', 'fc92ee87-5602-42f3-b201-1968e2857247', 'IMAGE', 'https://cdn.chotot.com/Jurst1JlSRDKcziYQlsX0fmkbtqD7NEwWrNKsHLeDlo/preset:view/plain/3e0893b5da77e095f56d83c5675532a3-2996120963749923193.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cd3e6ed2-abcc-4b02-8d46-5692eccd7b77', 'fc92ee87-5602-42f3-b201-1968e2857247', 'IMAGE', 'https://cdn.chotot.com/IILsUaxDzep4p61aiic0MpWKxWLrl13MGCGMaXM1_TU/preset:view/plain/351760be14580da40730dd8e35449f4e-2996120963897172056.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2ff7ae86-2e29-47ce-b4c1-bdd59ed73c80', 'fc92ee87-5602-42f3-b201-1968e2857247', 'IMAGE', 'https://cdn.chotot.com/fuuXJe-LbMiFm4EQtn_X50MN5lch6NQrFcb3NZFAMnU/preset:view/plain/e440662030fca8b71724dbda7296196d-2996120963775478509.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d9eebad9-bacc-4018-ac2c-07b65c32f04f', 'fc92ee87-5602-42f3-b201-1968e2857247', 'IMAGE', 'https://cdn.chotot.com/BFVlIljYZ8xZj4nXDkG-MmUB18FV9hKegIQmo4Y9jUE/preset:view/plain/3d80ccfb17ff53117344fb4e62570d9a-2996120963905201188.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('84048120-d59c-4b6d-9bf8-7a70e7c47dfe', 'fc92ee87-5602-42f3-b201-1968e2857247', 'IMAGE', 'https://cdn.chotot.com/g8MWS8inHMXQmbz8nSmQuDO86szWcWZpv8wOnAs235c/preset:view/plain/4241dd00f486fe44702ce52b6140d770-2996120964215695014.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d46f82e8-829d-4d40-b518-f859427cfe87', 'fc92ee87-5602-42f3-b201-1968e2857247', 'IMAGE', 'https://cdn.chotot.com/YLlxLPxDfidmAHhQBjs4OGoyEd2h4VEHkwc1ZLMlxKw/preset:view/plain/778040e716541863d88162cb452158cb-2996120964444967935.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('140f9ba9-bce1-41d1-aa91-683110486551', 'fc92ee87-5602-42f3-b201-1968e2857247', 'IMAGE', 'https://cdn.chotot.com/lbW7BxGEPpRzuv5gHf7UpWoCZ19JEKnag1uVzFgc7Xg/preset:view/plain/302179b0a222913dd266799f08cdcb82-2996120964501706833.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('133277b9-eb9e-46e8-a0dd-7a4ee50b86a9', 'fc92ee87-5602-42f3-b201-1968e2857247', 'IMAGE', 'https://cdn.chotot.com/jgBA-Pi6GeNMVQ7DaD7LPRcjVXC53Ut5thwgVjrDT58/preset:view/plain/b7b1f36b4f6996ba6dcc98eba089e662-2996120964065152615.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('460e5f8f-e1c5-4dcd-9143-19861ea24bbe', 'fc92ee87-5602-42f3-b201-1968e2857247', 'IMAGE', 'https://cdn.chotot.com/fNRHZ_dvz4DkNO4wnBZBJxiSew1rHaHNDz6gZ5NKCTk/preset:view/plain/bfc41030ba28483412f6de05cd0c1a53-2996120963914849175.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('e0421ed0-77fc-4a5e-a327-a4f971434655', 'P_124264584', 'APARTMENT', 'CĂN HỘ BAN CÔNG SIÊU ĐẸP NGAY TRƯƠNG VĨNH KÝ - TRẦN HƯNG ĐẠO TÂN PHÚ', '✨✨CĂN HỘ BAN CÔNG SIÊU ĐẸP NGAY TRƯƠNG VĨNH KÝ - TRẦN HƯNG ĐẠO TÂN PHÚ 🍃🍃

Ban công Cửa sổ giá từ 5tr5 6tr2 7tr5

🌵Địa chỉ: Trần Hưng Đạo, Phường Tân Thành, Quận Tân Phú

📌 Nội Thất: Đầy đủ như hình

👉 Phòng nội thất cao cấp xịn xò
👉 Nhà mới, nội thất mới 100% cực kì sạch sẽ
👉 Hầm để xe siêu rộng
👉 Giờ giấc tự do, Camera an ninh 24/24

📌Chính sách dịch vụ và quy định của tòa nhà:
+ Điện: 3.800đ/kwh
+ Nước: 100K/ng
+ Xe : Free

☎️☎️ LH trực tiếp qua Thuỷ Tiên ( ZALO/CALL ) để dc tư vấn - book phòng trên toàn khu vực', 'SOLD', 'Quận Tân Phú, Tp Hồ Chí Minh', 50, 5500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7dab64cc-20f3-4e39-9a6c-b92b4ddf617a', 'e0421ed0-77fc-4a5e-a327-a4f971434655', 'IMAGE', 'https://cdn.chotot.com/dMtrhmVh6RiF0N7c9gJMAhNfUzO6ACTV_j3qqel0ZoU/preset:view/plain/d045b5b136026927bb595fd66dcbdaec-2926722373137755187.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('207f968b-42c8-4568-8ab6-8e2eb2a8df19', 'e0421ed0-77fc-4a5e-a327-a4f971434655', 'IMAGE', 'https://cdn.chotot.com/thWDUFJjsS7nKn65kkbKc6G1W19asd58HxaUIS_r28U/preset:view/plain/131bd1d881de29570daf5eb56c895bd5-2926722373314565606.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5357a4a3-a153-4064-9f79-e657be8b2284', 'e0421ed0-77fc-4a5e-a327-a4f971434655', 'IMAGE', 'https://cdn.chotot.com/sGy_WvMe4Md55z3LLJmmHYun9vW1t5IeCcfSoiGdkuU/preset:view/plain/9f996f79cd204af24aed3355869cccc2-2926722373016954384.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('30e67b66-5092-4d9a-a3f3-b8b53b761c16', 'e0421ed0-77fc-4a5e-a327-a4f971434655', 'IMAGE', 'https://cdn.chotot.com/I2OvzAXLGDCUXJjRkYxr7TsABePPIeZSRopwkJiABDY/preset:view/plain/6b8300b42cc2fb2574a6ea344c1d9a9a-2926722373415652222.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('eaaf5356-7b68-40b3-a9ed-c208a45fe38a', 'e0421ed0-77fc-4a5e-a327-a4f971434655', 'IMAGE', 'https://cdn.chotot.com/WT_qdT4JoKzehBtB0Cn024FhkWBN00OkqUV43Cya2nQ/preset:view/plain/191d5e294bcf04e880d02cb5ef6bb60f-2926722373393182803.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('00b19a38-4ed1-48e4-97af-42bb9dfcd5db', 'e0421ed0-77fc-4a5e-a327-a4f971434655', 'IMAGE', 'https://cdn.chotot.com/8zLKobKTl-57fO5EtuvMsykNJcfdGo0HN_5_1lSNQDk/preset:view/plain/49c4466a52827d0df497bdbfb75c2eaf-2926722373654153727.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('705568bc-aa62-4c4c-8e16-1c8ff7363b87', 'e0421ed0-77fc-4a5e-a327-a4f971434655', 'IMAGE', 'https://cdn.chotot.com/-NmpQdyA6RT0xewZfVJniV1HIwxgu7_2rcDVUv1J_r8/preset:view/plain/7de797a27a174f930e9aea4d5881b3f7-2926722373456662041.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('361f859c-7834-4adc-9af0-5ed5c28bbeba', 'e0421ed0-77fc-4a5e-a327-a4f971434655', 'IMAGE', 'https://cdn.chotot.com/_JAORt-dTE5XmnyShQhfyG80UUYn3ykWE5aIZGrkdTo/preset:view/plain/dd5d9cd1fb60f01c59e9708b74735de1-2926722373512462050.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('50a21b8a-7944-4e8a-8aca-6a0d2691c138', 'e0421ed0-77fc-4a5e-a327-a4f971434655', 'IMAGE', 'https://cdn.chotot.com/xgmDxzLux04zeP--dbBodYZb9jnovw18Ixr_A3sitL0/preset:view/plain/e058062580e5a3dbdbb360f07637de30-2926722373438967947.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6736b139-5673-4076-a718-744ed120757b', 'e0421ed0-77fc-4a5e-a327-a4f971434655', 'IMAGE', 'https://cdn.chotot.com/84W5VJzFhwaX39CEhNuphieN11nBSyTSfJTQ0HYudqA/preset:view/plain/583719bbd465f37c35f2e31aefbf3094-2926722373489795844.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a1948524-7154-4aef-8dbf-9732150f4fcd', 'e0421ed0-77fc-4a5e-a327-a4f971434655', 'IMAGE', 'https://cdn.chotot.com/lJG5mdeysk2b7CkalbnZRatIe30KIG3Q2mWecJIysgA/preset:view/plain/1342aedea49cbd825a29b9a89b7869b7-2926722374126625740.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9acd71ef-22e2-4e6e-9546-5f451a374b41', 'e0421ed0-77fc-4a5e-a327-a4f971434655', 'IMAGE', 'https://cdn.chotot.com/th8Yt9G3Bo4chfudCK1GztEYWr1ZG-bv4oHAjJyaeo8/preset:view/plain/a4e3afbf802589267ded41b6cca0fe00-2926722373439151314.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('3dde09ae-2be0-45bd-95b4-01226480a7c2', 'P_133940387', 'APARTMENT', '🥰Căn Hộ Quận 7 -1Pn Đủ Nội Thất Ngay Quận 7', 'Dự án: 
Thông tin chi tiết: 🏙Căn Hộ 1 Phòng Ngủ Ngay Trung Tâm Quận 7

Địa chỉ 36a Đường số 2 Quận 7 - Cách lotte Mark 500m



✨ Tại đây, mỗi buổi sáng thức dậy, bạn có thể ngắm nhìn Sài Gòn nhộn nhịp ngay dưới chân mình.



🌿 Ban công rộng 6m – nơi bạn có thể nhâm nhi cà phê, chill cùng bạn bè hoặc đơn giản là tận hưởng khoảnh khắc một mình giữa không gian mở.



Ưu đãi này chỉ trong 5 ngày – vì chúng tôi đang hoàn thiện những chi tiết cuối cùng cho căn phòng độc nhất này.



🚗 Vị trí vàng – Ngay cầu Kênh Tẻ, thuận tiện đi lại



Chỉ vài phút để kết nối Quận 1, Quận 4, Quận 7.



Xung quanh đầy đủ tiện ích: ăn uống, mua sắm, Lottemark



👉 Căn phòng này không dành cho số đông – mà chỉ dành cho chủ nhân thật sự xứng đáng, người muốn biến nơi ở thành một trải nghiệm sống sang và khác biệt.



📞 Liên hệ ngay Quốc Thăng QUẢN LÝ NHÀ để không bỏ lỡ cơ hội hiếm hoi này.', 'SOLD', 'Quận 7, Tp Hồ Chí Minh', 35, 6500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('91d220dd-1008-4b5b-b261-f7336f586de0', '3dde09ae-2be0-45bd-95b4-01226480a7c2', 'IMAGE', 'https://cdn.chotot.com/wunCz4c4B2VzP-BPGc9qJMt5C5d2vLF9Za75qnQnQVI/preset:view/plain/6c1afd147c201109c7cdf19d8d5e2a32-2996120952908585041.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('04b90032-e6b6-4c6f-a1f2-43b3e35b11a6', '3dde09ae-2be0-45bd-95b4-01226480a7c2', 'IMAGE', 'https://cdn.chotot.com/kYcDJtZykJ9bQGzt9F5FMwnjOUB37sE7sZOX7jS85bk/preset:view/plain/911a519cacd5a53ed8406eec778376e1-2996120953025405016.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('570f7e92-5d9c-47eb-9045-405bcf5b707b', '3dde09ae-2be0-45bd-95b4-01226480a7c2', 'IMAGE', 'https://cdn.chotot.com/6Q6TZf_a56kJVLfnEnIHu9qKr9Iut6cWQlLcaql1hJs/preset:view/plain/29796629f5db63dd4d4c2a1c3521fda4-2996120952925015655.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ce8b1716-afc8-4597-9f6a-e2825a7f2e51', '3dde09ae-2be0-45bd-95b4-01226480a7c2', 'IMAGE', 'https://cdn.chotot.com/JYtnHuu7a6joy5YLFdOObkRee1Yj706axEuhHmyiXbU/preset:view/plain/b590c8c771b0cd3fc05bb867a9ae0daf-2996120952924563110.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('b495273f-d5c1-41d8-9ed6-c83d7fc50c30', 'P_133600499', 'APARTMENT', 'GIÁ THẬT- CĂN HỘ 1 TRỆT 1 LẦU RẺ Q7, GIÁ ĐỘC QUYỀN KHÔNG AI CÓ', 'Dự án: 
Thông tin chi tiết: Sáng tập Gym, tối đi bơi tại căn hộ 1 trệt 1 lầu giá tốt trung tâm quận 7
Không đăng giá ảo, giá thật hình thật, qua xem là còn phòng, k còn k cho qua xem
Gần Phú Mỹ Hưng, KCX, Lotte, Crecent Mall
Gần KCX, UFM, PMH, CRESCENT MALL 
Gần LOTTE, UFM, TDT, Q4, CẦU KÊNH TẺ 

- Tại Nguyễn Thị Thập quận 7

- có phòng gym, hồ bơi, sảnh phòng khách...

- Cư dân văn minh và hiện đại

- Có bảo vệ, an ninh 24/24 

- Nhận người nước ngoài

- dịch vụ dọn phòng free hàng tuần

- Studio 16m2 6 🍠
- Studio 19m2 6🍠8
- 1 trệt 1 lầu basic 6🍠8
- 1 trệt 1 lầu plus 7 🍠 3', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 30, 6000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('34d6f3b1-c83c-45c9-a85e-6a6572fdddd6', 'b495273f-d5c1-41d8-9ed6-c83d7fc50c30', 'IMAGE', 'https://cdn.chotot.com/X5FUIjo2wy4zOyGyf-BjNzWxMvvkS2vD6xF-WHwEz9s/preset:view/plain/ead6c3476ad650e60e145073dc697d99-2994107465435249855.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2b79537c-3d52-4b4d-bec4-4dd990fbd568', 'b495273f-d5c1-41d8-9ed6-c83d7fc50c30', 'IMAGE', 'https://cdn.chotot.com/QefDJ65_yU4YZrelNYexaNVYMa4Tjv5OI0_Ls0BEHkI/preset:view/plain/8417da471265b24e6dc2f9ef94c52415-2994107465770004920.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('10180144-b4b5-4ba5-ab24-cd1dcdfe45d3', 'b495273f-d5c1-41d8-9ed6-c83d7fc50c30', 'IMAGE', 'https://cdn.chotot.com/9prkOa-spd25CW41pE4NbZU7rzxjLohuygmzRGO-EfI/preset:view/plain/fea7b64f91427e83a2ef85fcbed41573-2994107466755703967.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e2e6c182-0652-4e46-af51-07d64a200c36', 'b495273f-d5c1-41d8-9ed6-c83d7fc50c30', 'IMAGE', 'https://cdn.chotot.com/L0j-1HU-ydRUX0jucxqRe6rFodcksKBxq8baXOEfl4U/preset:view/plain/da258ced2f88242022ef61a5bcf37eb2-2994107466906580158.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f4affea8-97fb-4693-a26a-40c65b46e38a', 'b495273f-d5c1-41d8-9ed6-c83d7fc50c30', 'IMAGE', 'https://cdn.chotot.com/bN-Gj-D_zMU2Pc76wSd10o4muL7v_H7uBt_LkziirsE/preset:view/plain/20b20425144a75cf6df22abed52821bf-2994107466906081930.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8ac80eb9-f789-4ef2-988b-078964bf899c', 'b495273f-d5c1-41d8-9ed6-c83d7fc50c30', 'IMAGE', 'https://cdn.chotot.com/_sxjA17Hb4lBYrZykvxfGyUB5dNyO1JRhb0lCSHTI6M/preset:view/plain/022e0cde7702d382bdcdddd27279524f-2994107466765016607.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dbb237f8-c525-4606-9413-4a4d5c4652c7', 'b495273f-d5c1-41d8-9ed6-c83d7fc50c30', 'IMAGE', 'https://cdn.chotot.com/p4s74mIYmYv2LaFpQrv361oyLd3Wf_1SKtAoDVsesas/preset:view/plain/19475868de99598971ddfea4ec86e09a-2994107467498019014.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a0c7d248-628f-417d-a475-c9e97423493d', 'b495273f-d5c1-41d8-9ed6-c83d7fc50c30', 'IMAGE', 'https://cdn.chotot.com/cgZZ6NPeFvsxwAJP3eqspm__hcLVlNUw5xRfYi1O9AE/preset:view/plain/92a172e6bc1b907432e64420be6998a2-2994107467136734969.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9a5b43fe-cf23-49b9-a38c-c164c719b2f4', 'b495273f-d5c1-41d8-9ed6-c83d7fc50c30', 'IMAGE', 'https://cdn.chotot.com/FeJwjTxJOvxeQR1TVPAazBZrP4Xb4ykKVlS9vIorBPA/preset:view/plain/97d490b288629e2a81c58b7bc815e580-2994107466951761886.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9a451f43-542d-44ac-975f-6ebfafdb8373', 'b495273f-d5c1-41d8-9ed6-c83d7fc50c30', 'IMAGE', 'https://cdn.chotot.com/2THLgIhQBU_Ulw8-Pd6vy3ARISI9pwdw1IQhDbJ_DGc/preset:view/plain/5eda05c60456c14ae649204b0bdf9c38-2994107467253842360.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b9e8f4c8-78ed-4839-8aa3-5fc8c9fb636d', 'b495273f-d5c1-41d8-9ed6-c83d7fc50c30', 'IMAGE', 'https://cdn.chotot.com/7OTzf_WOYwwts350FUQdpptLMkxQif1lIhuNlTzjTDw/preset:view/plain/b8584dca8d510f1cba7798a4ba36cc66-2994107466981513752.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ca871401-26dd-483d-bc89-d6a70a6f31e5', 'b495273f-d5c1-41d8-9ed6-c83d7fc50c30', 'IMAGE', 'https://cdn.chotot.com/9xESXxhd1M_zlSVTf3ni8_mDCq-rPOfQljWQROlqCL0/preset:view/plain/c6ca0214010e35a9209a165de2122dcf-2994107466918520662.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('819828ab-44b6-4d48-9864-de4700a73d55', 'P_133940376', 'APARTMENT', 'Bao thuế phí 1PN+ view thoáng Vinhomes Grand Park có thương lượng', 'Dự án: 
Thông tin chi tiết: Thiện chí khách đến xem và có thể thương lượng.
Căn hộ 1PN+, 1WC. Nội thất bàn giao như hình: tủ bếp trên dưới, bếp rèm, máy giặt sấy, tủ lạnh, tủ liền tường.
Nhà đã dán cách nhiệt, mát mẻ, 
Tiện ích và dịch vụ khối đế lấp đầy
Gần trường học
Gần quảng trường, Vincom Grand Park', 'AVAILABLE', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 57.2, 2850000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('65accd9a-d28b-4adf-8cdf-9282e6ea0196', '819828ab-44b6-4d48-9864-de4700a73d55', 'IMAGE', 'https://cdn.chotot.com/4fXf5Xh8wrxrWQ6DNsH6ZggYq5HkCv6gYONLmGX9CDw/preset:view/plain/d8241cf11a348e346e5c5e4b362e275b-2996120402260009048.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('551913e5-5810-4d67-a935-a5cb8b733db4', '819828ab-44b6-4d48-9864-de4700a73d55', 'IMAGE', 'https://cdn.chotot.com/QFpaWjo9Bysttoa6uLrJRzHlfgcSi4t0GRxsnWeXeK4/preset:view/plain/ba553c8959df3cf34e4195ca65ddcf16-2996120403082515752.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('027792a9-7835-4595-b5c7-e9030bfc1eac', '819828ab-44b6-4d48-9864-de4700a73d55', 'IMAGE', 'https://cdn.chotot.com/ZgKADkrjiPxIV3C4tR5pScfQN9fgNK_KgxJreA39akk/preset:view/plain/774a4d73e24f742b07c64a5884b36631-2996120403536477709.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7b20eb71-0bf4-4cc3-b5cc-a2a0ab43f199', '819828ab-44b6-4d48-9864-de4700a73d55', 'IMAGE', 'https://cdn.chotot.com/_8C79RTgr-6JtFdt6cR-ExnWbrvTdPDtuASpeJPKDU0/preset:view/plain/5b8a08ff2abefb36108c34a25f105b2a-2996120403386358679.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e0e9786f-3794-4524-8c5c-19c198f90f28', '819828ab-44b6-4d48-9864-de4700a73d55', 'IMAGE', 'https://cdn.chotot.com/tznB1cm--eUkVf-N6kDSrE_I7Oqknwa7WA74TnUMGAk/preset:view/plain/8979df32e66eabc421a4d1ce20ef1773-2996120403418000339.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('676cb3dc-4d01-436f-9d03-60f1dc598ce7', '819828ab-44b6-4d48-9864-de4700a73d55', 'IMAGE', 'https://cdn.chotot.com/1An-Q3zKP3j_45nROtKNIxCWO_XTQIc-b34OPShTqS8/preset:view/plain/f5540cb10b704fd29d161fa1866a3430-2996120403403982308.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d15cfcbb-fdde-4ee2-b515-3c39e5240c43', '819828ab-44b6-4d48-9864-de4700a73d55', 'IMAGE', 'https://cdn.chotot.com/rtvRuxJ_7ywZOusslJE5TtdY1Sh3iwd4B569aGtOzAw/preset:view/plain/d665054eeaef6c487d0e08f9e6703cf4-2996120403838933073.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('578e3ddf-a980-441e-8e90-a9b1f1ad3fd2', '819828ab-44b6-4d48-9864-de4700a73d55', 'IMAGE', 'https://cdn.chotot.com/dRYXpO17zsUv0sKkYfQDOKeFLvwsMnbwPf2GkOidzVY/preset:view/plain/b495448fb3152ba0d87c06397d49ceda-2996120403864835071.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('3e5361dd-29c0-4874-94fe-a91d7751f06f', 'P_133940374', 'APARTMENT', 'CHO THUÊ CĂN HỘ QUẬN 10 MỚI 100% –STUDIO BAN CÔNG RỘNG - Full Nội Thất', '🏡 CHO THUÊ CĂN HỘ DỊCH VỤ QUẬN 10 MỚI 100% – STUDIO BAN CÔNG RỘNG – FULL NỘI THẤT ✨

🔥 Bạn đang tìm phòng trọ Quận 10, căn hộ Quận 10, studio Quận 10 hoặc căn hộ dịch vụ gần Đại học Bách Khoa? Đây là lựa chọn rất đáng xem!

✅ Căn hộ mới 100%, thiết kế hiện đại, sạch đẹp.
✅ Ban công riêng rộng rãi, đón gió và ánh sáng tự nhiên.
✅ Full nội thất: Máy lạnh, tủ lạnh, giường, nệm, tủ quần áo, bàn ghế...
✅ Máy giặt riêng từng phòng.
✅ Điện chỉ 3.500đ/kWh.
✅ Dọn vào ở ngay.

📍 Địa chỉ: Đường Tô Hiến Thành, Quận 10 (khu Hòa Hưng), TP.HCM.

🚗 Chỉ vài phút đến:
• Đại học Bách Khoa TP.HCM
• Đại học Sài Gòn (SGU)
• Đại học UEF
• Thành Thái
• Đường 3 Tháng 2
• Bắc Hải
• Công viên Lê Thị Riêng
• Di chuyển nhanh sang Quận 5, Quận 3, Quận 11 và Tân Bình.

💯 Phù hợp cho:
✔️ Sinh viên
✔️ Nhân viên văn phòng
✔️ Người đi làm
✔️ Cặp đôi
✔️ Người nước ngoài sinh sống tại TP.HCM

📲 Liên hệ xem phòng ngay: *** – Kim Lân

🏠 Ngoài căn này, bên mình còn nhiều phòng trọ Quận 10, căn hộ dịch vụ Quận 10, phòng trọ Quận 5, studio, Duplex, phòng gác lửng, 1PN, 2PN, 3PN, phòng có ban công, cửa sổ lớn... với nhiều mức giá phù hợp cho sinh viên và người đi làm.

#PhongTroQuan10 #CanHoQuan10 #CanHoDichVuQuan10 #PhongTroQuan5 #CanHoQuan5 #StudioQuan10 #PhongTroGanBachKhoa #ChoThueCanHo #ChoThuePhongTro #CanHoDichVuTPHCM #TheRoomSG', 'AVAILABLE', 'Quận 10, Tp Hồ Chí Minh', 30, 8000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b20dd2a9-bc89-41b9-83b6-8168ff6e1189', '3e5361dd-29c0-4874-94fe-a91d7751f06f', 'IMAGE', 'https://cdn.chotot.com/1K81bV7p2nh8V-KpA_ptHFZ8bEtENd9UYxqkTxKtNzU/preset:view/plain/d0b62bcfab2c5f37c84f47066cffa416-2996120409814049828.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d3c0594c-d8ec-4e87-8c19-43269b45e7cf', '3e5361dd-29c0-4874-94fe-a91d7751f06f', 'IMAGE', 'https://cdn.chotot.com/wYRH-QO5e5JmOrf3drd2n9Cv2ho52PX1h17gJlaQ9sY/preset:view/plain/9ae9891addc876677e9f1e869087ee40-2996120409799867117.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('54991ad6-9135-473b-aa23-7de458feb1de', '3e5361dd-29c0-4874-94fe-a91d7751f06f', 'IMAGE', 'https://cdn.chotot.com/M1xbbT1GbB9waLbLax07O8QQ-2tT6DfSXyLJVzSz1MM/preset:view/plain/70db06ce9d55293b97c763b75a7c6288-2996120411220823655.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('eeab4e38-b783-41f9-89d1-faa58cd992ac', '3e5361dd-29c0-4874-94fe-a91d7751f06f', 'IMAGE', 'https://cdn.chotot.com/dBO46gviD7lD24EnXZ2XNiE649YdmslWVFZML3NpPBU/preset:view/plain/e1e42359ee034f56fad133e846dab0bd-2996120411290510372.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9c76cddf-1b54-41f4-ba03-69d5a270d9fd', '3e5361dd-29c0-4874-94fe-a91d7751f06f', 'IMAGE', 'https://cdn.chotot.com/BXsDUElR4-bUcywzj7ZIlA_rUuLUx63WK6P2qyfTJdo/preset:view/plain/3ed3779e35cfd5273127e7e176e8e5f9-2996120412595393832.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('a8119d3f-d1bc-4706-8bbb-986ee182147f', 'P_130364871', 'APARTMENT', '⭐RIVER PANORAMA CHO THUÊ 3PN2WC 90m2 NTCB GIÁ CHỈ 14 TRIỆU', '- Cho thuê căn 3PN2WC 90m2 tại chung cư cao cấp River Panorama 89 Hoàng Quốc Việt, Quận 7 Giá Chỉ 14 triệu .

- Thiết kế: 3PN2WC, ban công + lô gia

- Giá thuê: 14 triệu /tháng

- Tầng cao, ban công view sông và thành phố đẹp lung linh

- NTCB gồm: Rèm, máy lạnh, máy nước nóng, bếp điện âm, máy hút mùi, tủ quần áo, tủ giày, thiết bị nhà vệ sinh đầy đủ

- Căn hộ đang trống có thể dọn vào ở ngay

- Sẵn pass xem nhà mọi lúc

- Tiện ích cao cấp: Hồ bơi vô cực tầng thượng đỉnh, phòng xông hơi, BBQ, khu vui chơi trẻ em, khu ngắm cảnh tầng Long Môn...

- Điện, nước, cáp nét: Theo hóa đơn nhà nước.

Ngoài ra em còn các căn diện tích khác giá tốt thị trường:

* 2PN-1WC (55m2): NTCB Giá từ 10 - 10.5 triệu/tháng, full nội thất từ 11 - 12 triệu/tháng.

* 2PN-2WC (64m2): NTCB Giá từ 11 - 11.5 triệu/tháng, full nội thất từ 13 - 14 triệu/tháng.

* 3PN2WC (114m²): NTCB từ 16- 17 triệu/tháng, full nội thất từ 20 - 25 triệu/tháng.

Liên hệ ngay Huy (call/zalo) để được tư vấn và tham quan căn hộ 24/7', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 90, 14000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('24918033-fe77-41f8-8773-e56c36887fd1', 'a8119d3f-d1bc-4706-8bbb-986ee182147f', 'IMAGE', 'https://cdn.chotot.com/ZNvlmGAXcRBLS2kz4BIuAkCOn3KAnZK89f1kEpT4WtU/preset:view/plain/c2fcb3700709ab419ba820df59df6d8a-2973786236111628062.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8502c669-3fb0-4561-9aad-52a25813e194', 'a8119d3f-d1bc-4706-8bbb-986ee182147f', 'IMAGE', 'https://cdn.chotot.com/3cBvnC4O27_uRYLtw90UwboNf672BelpGXJZouNIG80/preset:view/plain/86de0b22f0635b3621ab72702532ce82-2973786243124569886.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('32ee05ed-75a2-4b92-a422-6212e43f5eec', 'a8119d3f-d1bc-4706-8bbb-986ee182147f', 'IMAGE', 'https://cdn.chotot.com/GpL2dySz4uJUq0krwhNLyPIRLsvnwyBFdoQEYL3UsV4/preset:view/plain/5914762b2049df7b5b7bb1a19e698b38-2973786253778222498.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('09446f44-1f5e-4faa-b9d0-ec74e6b61abe', 'a8119d3f-d1bc-4706-8bbb-986ee182147f', 'IMAGE', 'https://cdn.chotot.com/zM5nRXdK_ddXbrEPa005oTobLn85tMLw9GfInmMQhEk/preset:view/plain/ec095d43f4bb2de67ce8e9a78f4cbae9-2973786293154872738.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5db59165-24e5-4d02-8f98-1dcbcbaa09a5', 'a8119d3f-d1bc-4706-8bbb-986ee182147f', 'IMAGE', 'https://cdn.chotot.com/3krklPUnzlI0Q2FEfAi7aX7woidZUof8hmIdo3mW4CQ/preset:view/plain/ac15966ea64f5572471b26522662f38c-2973786293222123294.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9a86605f-e9a1-467a-ae37-55e6988a2fcd', 'a8119d3f-d1bc-4706-8bbb-986ee182147f', 'IMAGE', 'https://cdn.chotot.com/02NGJegUhprOG7ITPemcQY1f_ptnwRV8KO4HjrIWBqY/preset:view/plain/7a49600ba57686521ead12e0e646f56c-2973786293158873967.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('66a8ae40-5da8-4c08-8c27-37d0232cdae0', 'a8119d3f-d1bc-4706-8bbb-986ee182147f', 'IMAGE', 'https://cdn.chotot.com/cBssEY-ovPyEHkAiXjzYk6OGwJEW-DcolXrEH1anxlg/preset:view/plain/9da7ad35361d1239a4506d57b01267b9-2973786293329156508.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5087b66d-1b6e-4784-a250-cd8bae7331a0', 'a8119d3f-d1bc-4706-8bbb-986ee182147f', 'IMAGE', 'https://cdn.chotot.com/jm-HQU9jXRFtCQ7Y6j4-Hwu5StFbb44qNPHjKZE32us/preset:view/plain/59770e093a6c70ce36eea713d31c0f42-2973786396336858910.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('753cf144-8a45-46f1-a18d-94d03d51e484', 'a8119d3f-d1bc-4706-8bbb-986ee182147f', 'IMAGE', 'https://cdn.chotot.com/41WAa7sy3WZpRpFNszXLxbTXORzTz2FXSTS9Kq7Z-RQ/preset:view/plain/1c082b4cd4c12a5df41850055221d7c7-2973786595452059042.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4a8283fb-9e6a-4233-9c79-7eee2402acb4', 'a8119d3f-d1bc-4706-8bbb-986ee182147f', 'IMAGE', 'https://cdn.chotot.com/kdLzUTGtpxSm-nzUzhOvfKq-3_4Radfo0rYLtC-yWPY/preset:view/plain/882a29f7bc56f1982b4be1acc41e1140-2995958238843963988.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('92d74cdf-3ba8-412f-a753-8fa122855593', 'a8119d3f-d1bc-4706-8bbb-986ee182147f', 'IMAGE', 'https://cdn.chotot.com/VPT1t23QOwtvCbmzEBgfc-oi3_scouGD-BNCUnnsbpw/preset:view/plain/a4c9a635d1afe1879d4c9313ecd7793e-2967554684877613089.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('895b478c-31e6-4e18-b364-d8cb9b81bb30', 'a8119d3f-d1bc-4706-8bbb-986ee182147f', 'IMAGE', 'https://cdn.chotot.com/iBK76wXtTOt8f4sBS1q4LB39KOeDbb82gDbE9VPFAh8/preset:view/plain/f564092be84473e16f3a52c3e831e75f-2967554684404663304.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('f3aeb4ec-742c-44f2-a144-9c697871f7de', 'P_133745014', 'APARTMENT', 'chính chủ cần bán căn chung cư quận 4', 'Bán gấp chung chư phường 3 quận 4 .gần chợ ,trường học ,công viên khu vui chơi .giao thông thuận tiện  ,gần quận 1 .liên hệ chính chủ ***', 'AVAILABLE', 'Quận 4, Tp Hồ Chí Minh', 44, 1750000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a59c1620-846e-484a-9b37-402cb7d4c963', 'f3aeb4ec-742c-44f2-a144-9c697871f7de', 'IMAGE', 'https://cdn.chotot.com/E48xqdLY3bTx3D7amPs4fQX5jCfaZ789BAIpQvOc_3k/preset:view/plain/5bd14efb6287a6a982cc4e474772fec1-2994646519474179201.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('02a1b4f9-c63f-4bf6-9bde-85babeac34ab', 'f3aeb4ec-742c-44f2-a144-9c697871f7de', 'IMAGE', 'https://cdn.chotot.com/4ITJnl8N2C4EkOY31iYAliXaqk30q5m0MIdFeR3Vp8U/preset:view/plain/51b094e8ef83722236748fd50c91f35a-2994646519603325185.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a22e7d15-6f95-44bf-b3cc-af58a00ddaf5', 'f3aeb4ec-742c-44f2-a144-9c697871f7de', 'IMAGE', 'https://cdn.chotot.com/Jp-q3j2rD_twRPB6iuFan00IowSsbJ9kY6F8qpNYFHQ/preset:view/plain/687d7293fb2283a3382ea11f512b0566-2994646519807943393.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('53c22c48-b66a-4cc9-a83d-476f317321bc', 'P_131169757', 'APARTMENT', '2 pn CH central garden quận 1 cho thuê', 'Cần cho thuê căn hộ Central Garden Quận 1
 ***DT 87m,  2phòng ngủ, 2WC, nhà thoáng mát sạch đẹp căn góc.Cho thuê 16 tr/ tháng 
 ***Dt  76m, 2 phòng ngủ 2 wc, nội thất đầy đủ,cho thuê giâ  từ 14 tr/ tháng thương lượng 
☎️ Liên hệ xem nhà -', 'UNDER_OFFER', 'Quận 1, Tp Hồ Chí Minh', 84, 14000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3c6cb256-246e-4c83-b531-9147ab1dcccd', '53c22c48-b66a-4cc9-a83d-476f317321bc', 'IMAGE', 'https://cdn.chotot.com/s0aX_-p0npnTFUluR0VZpwj6KDyBiEryVeolID_4v-s/preset:view/plain/a4d43fec62f4fd5d89248406a635a87a-2977970641889667386.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ebe8c1d8-f687-48fa-8f22-b827913d9025', '53c22c48-b66a-4cc9-a83d-476f317321bc', 'IMAGE', 'https://cdn.chotot.com/iHXC1Suz7UILTTyn-sRGsKKvdYmUVqABtGlLSQaUOnI/preset:view/plain/c263dbaa248533f63097862c4f93daba-2977970641613348550.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f0ed9856-dd2f-4310-b5c9-86ba7459edb8', '53c22c48-b66a-4cc9-a83d-476f317321bc', 'IMAGE', 'https://cdn.chotot.com/vLL-t3UhNJBhaGJ7eWuWJ4r7kwp1RfTrEZhJnrjxTOs/preset:view/plain/6f35e483bba614d818dc4d3642d6c619-2977970643014600374.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('871c8060-472e-4d5c-b39e-d40af4ff2796', 'P_123170673', 'APARTMENT', 'CĂN HỘ CAO CẤP 1PN TÁCH BẾP FULL TIỆN NGHI_NGUYỄN VĂN LUÔNG_MEGA Q6', 'CĂN HỘ CAO CẤP FULL NỘI THẤT GIÁ RẺ HẬU GIANG  MEGA BÌNH PHÚ QUẬN 6 🫡

📍Hậu Giang, Mega Bình Phú , Phường 12, Quận 6

- Trang bị full nội thất đầy đủ tiện nghi mới
- Giờ giấc tự do, không chung chủ, camera an ninh, hầm xe rộng, khu giặt sấy riêng
- Free phí xe, rác, internet
- Cửa phòng vân tay, thẻ từ
- Ở được 2-3 bạn, phù hợp với sinh viên và hộ gia đình


‼️ Đối diện Trường cao đẳng Phú Lâm, Gần Vòng Xoay Phú Lâm ,thuận tiện qua các quận lân cận, xung quanh có nhiều cửa hàng tiện lợi, tiệm tạp hoá,... 

LIÊN HỆ ☎️ : 0828132xyz (Tuấn Võ Megas)
#canhocaocapquan6 #nhatrogiarequan6

#phongtrosinhvien #nhatrosinhviengiare
#phongtrosinhviengiare #phongtroquan6
#phongtrotachbep #nhatrogiare #canhodichvu
#canhoquan6 #canhogiare', 'SOLD', 'Quận 6, Tp Hồ Chí Minh', 45, 6300000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c5ac20c1-e015-4d26-890f-7b03a775e5fa', '871c8060-472e-4d5c-b39e-d40af4ff2796', 'IMAGE', 'https://cdn.chotot.com/R9qpwFmGmrSRkiUik1NHDD74jx3zuJyw_k5NsI06P-U/preset:view/plain/da3eb70b636a09ea55da3b24e2ce9380-2920349114795138837.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a4630d7f-364e-430f-acf1-e6783911d5c2', '871c8060-472e-4d5c-b39e-d40af4ff2796', 'IMAGE', 'https://cdn.chotot.com/kxxD_KsZx0XNbknrXZECdizgJkj2aFLpdhLnxLj9JZ4/preset:view/plain/9b6200c5b79320f2993fd9615a03d36f-2920349114868418884.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2028cef9-e8a0-47b1-814c-d86d10f98c65', '871c8060-472e-4d5c-b39e-d40af4ff2796', 'IMAGE', 'https://cdn.chotot.com/_PBuypJ5tostsxdT2qrDN11N5p4JB4ClusmWp40r0gc/preset:view/plain/a10902408edfb413575dedc6ed76771c-2920349114830292915.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e62f7946-3c9e-46c3-b8f1-880b555262ec', '871c8060-472e-4d5c-b39e-d40af4ff2796', 'IMAGE', 'https://cdn.chotot.com/Urnv3STXKxjrckoqM-Vzg_vl2CaK88gcbhrPj9BcYZA/preset:view/plain/4f97d474eaa6431c512d887d3779d6d4-2920349114910591493.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c52cc94e-a63d-4810-aad5-9202e15ad4a2', '871c8060-472e-4d5c-b39e-d40af4ff2796', 'IMAGE', 'https://cdn.chotot.com/Xif2xTj9D-klLPfxvvrOe4EHxw0xvwhdhXtyBRjj5y4/preset:view/plain/943caccf6f69612ea3a082448aa74299-2920349115001184442.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('34835991-65f5-4e7c-b691-68caedcb9cc0', '871c8060-472e-4d5c-b39e-d40af4ff2796', 'IMAGE', 'https://cdn.chotot.com/KuPiK5yvWYfZ9z4tG43tKSoscz5HpTvdFGul7ck_Uns/preset:view/plain/bff434db3058a7b9dcbfa8dbe9d42766-2920349114964574148.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a44b0e77-9de8-4c35-b8fb-9c327e7a13f8', '871c8060-472e-4d5c-b39e-d40af4ff2796', 'IMAGE', 'https://cdn.chotot.com/iyIfc6kH9Hc_-kFpthM3OSopJ4aTofWG2AI2TfV-DXM/preset:view/plain/545cd7a5d7fcd6e3085df4b2dc0a7631-2920349114955009207.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('8c48b308-950b-4bb8-9887-0d830205be86', 'P_131085596', 'APARTMENT', '✨✨ STUDIO CỬA SỔ THOÁNG THANG MÁY MỚI TINH NGAY PHAN XÍCH LONG - NGUYE', 'Tiện ích toà nhà:

+ Toà nhà với nhiều tiện ích chung, có người lau dọn hành lang bãi xe khu vực chung, có khu giặt sấy, có thang máy, bảo vệ

+ Phòng được trang bị đầy đủ nội thất gồm: Máy lạnh. Tủ lạnh. Giuong nệm. Tủ quần áo. Kệ bếp. Tủ bếp. Máy nóng lạnh,...

+ Hầm xe toà nhà rộng rãi, ra vào đi lại tự do, camera bãi xe hàng lang 24/7, trang bị pccc đảm bảo an ninh.

+ Khu dân trí cao an ninh, gần các cửa hàng tiện lợi, trung tâm mua sắm, khu sân bay, BV Tâm Anh,...

+ Thuận tiện di chuyển đi các địa điểm: CV Hoàng Văn Thụ, Vòng Xoay Phạm Văn Đồng, Vòng xoay Lăng Cha Cả, Dễ đi Quận 1 - Quận 3 - Quận 10 - Phú Nhuận - Gò Vấp - Binh Tân,...

Liên hệ: SĐT - Zalo - FB (Thái Thịnh).

Hỗ trợ tìm phòng và xem phòng khu vực Sài Gòn', 'AVAILABLE', 'Quận Phú Nhuận, Tp Hồ Chí Minh', 30, 4700000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a39b168c-3dee-4a0b-a748-c8345adb7735', '8c48b308-950b-4bb8-9887-0d830205be86', 'IMAGE', 'https://cdn.chotot.com/IZnDqkJjlKbmIrKvkt7bE4EiuQp_sE34fIWvdk5eBEs/preset:view/plain/392d8cbbd9715470cc4401237e4ebb63-2974663706951747930.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c36e51de-395a-4dfc-ad29-44be1a7d0fa9', '8c48b308-950b-4bb8-9887-0d830205be86', 'IMAGE', 'https://cdn.chotot.com/_-Zs_5z3EUrU1wVQmwGY_9znS2fFMFtejRm_VFFGB3w/preset:view/plain/92823ba02c37d05cb553f6d7e8e8d644-2974663708829027677.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('93b9f3ac-627b-4184-8075-a12be6e7a221', '8c48b308-950b-4bb8-9887-0d830205be86', 'IMAGE', 'https://cdn.chotot.com/lWjmpUzhg8kVb_KaGy7d9MkJmEDNVmcGUkfT5jyM3pY/preset:view/plain/4877976c147ddf562640821e2a578ae0-2974663709839328252.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c1e171b4-af25-4724-bf49-7fc2c013a875', '8c48b308-950b-4bb8-9887-0d830205be86', 'IMAGE', 'https://cdn.chotot.com/yeoAQrUbt5eqgl3CayvCm3ImDDYkuOmiFYfJ0uC4ntk/preset:view/plain/eab28129cacaf3ef88ae5fdf4f21a005-2974663711231963607.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8748c218-7535-493b-a525-eefcd54339f9', '8c48b308-950b-4bb8-9887-0d830205be86', 'IMAGE', 'https://cdn.chotot.com/l-fOLzq84dxqh7nYpW8nvvat6X9gQwoBYq0_ivnpPpo/preset:view/plain/b5428a045f075c8354163fc222c1b788-2974663711763545521.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('34b94114-97b9-4e99-b999-3045cbfbfeea', 'P_133940320', 'APARTMENT', 'Chính chủ cho thuê căn hộ Ascent Lakeside Q7, DT 50m2/1PN, giá 8 triệu', 'Cho thuê căn hộ Ascent Lakeside tiện làm văn phòng công ty.
- Diện tích: 50 m². View thoáng mát
- Kết cấu: nhà trống suốt, 1 nhà vệ sinh.
- Giá thuê: 8 triệu/ tháng.
- Tiện ích nội khu: Cabana thư giãn, hồ bơi nước ấm, gym, khu BBQ, công viên nội khu, siêu thị, An ninh 24/7, thẻ từ thang máy.
- Giao thông thuận tiện: Gần Lotte Mart, ĐH RMIT, chỉ 10 phút đến Quận 1.
* Liên hệ xem nhà ngay:  ms Nhung (call, zalo).', 'UNDER_OFFER', 'Quận 7, Tp Hồ Chí Minh', 50, 8000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8be70f12-4b2c-4ff5-9f3e-be0bbcc5fcfe', '34b94114-97b9-4e99-b999-3045cbfbfeea', 'IMAGE', 'https://cdn.chotot.com/dpYZaeW-GMnn0tnI203mNytfLfdAH5-qoFBSvO5eDsg/preset:view/plain/feb7774b1d31646a6a9b14e163b14a2d-2996120578326373412.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1ecbce1d-e95c-457f-b6d8-96725c2c88f1', '34b94114-97b9-4e99-b999-3045cbfbfeea', 'IMAGE', 'https://cdn.chotot.com/Y_c5EbQ5Td9ULdoALDbBnZb1dRRP-m6OyPTYL1sfGU8/preset:view/plain/2dd065cefcfec056c4807235bfa0f0cb-2996120589992317951.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8fd1b6a1-793b-415b-9a62-48ec45b50ca1', '34b94114-97b9-4e99-b999-3045cbfbfeea', 'IMAGE', 'https://cdn.chotot.com/Ou61PJLII1RgePUZ51_dUV-Vwbf3swir1h7shfeqpgc/preset:view/plain/cd1d4f972a93a9ddf475f319b2ba76f0-2996120598288110888.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5c8be258-ea2b-406e-8f1a-27ef7829fc44', '34b94114-97b9-4e99-b999-3045cbfbfeea', 'IMAGE', 'https://cdn.chotot.com/puXgbt7GUMk30973USxzb9Vqwr73C_xA893FzuORW4c/preset:view/plain/671a686a01b47fa32b349fac4f7b3298-2996120608790779176.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('a5a13b2b-6e1e-40a4-b821-a5e175d2097c', 'P_112014294', 'APARTMENT', 'Cho thuê CH gần cầu SG - Tiện nghi, thoáng mát - Full mới đầy đủ nt', 'CĂN HỘ FULL NỘI THẤT GẦN CẦU SÀI GÒN, ĐIỆN BIÊN PHỦ, CẦU THỊ NGHÈ, Nguyễn Thị Minh Khai, Xô Viết Nghệ Tĩnh, Cầu Thủ Thiêm, Sala Thủ Thiêm

Vị trí: Trần Não Ngay dưới chân cầu SG

Thuận tiện di chuyển qua BT, quận 1,3,10 trung tâm
Phòng hót mà Full nội thất chỉ 7tr5
Có thể ở liền
Ban công thoáng mát
Hầm xe rộng rãi
Bảo vệ, camera an ninh
Khu dân cư an ninh yên tĩnh
Được nuôi PET


Hifriendz hỗ trợ tìm phòng theo nhu cầu

Liên hệ mình để được hỗ trợ tìm phòng Q2 - Q9', 'AVAILABLE', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 30, 6500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e8779503-6b43-4444-aeb1-1522d631944a', 'a5a13b2b-6e1e-40a4-b821-a5e175d2097c', 'IMAGE', 'https://cdn.chotot.com/IwMrlFYqsa-ZYq7TWpE7QrCBchfXMUFCN2ryaqJypHA/preset:view/plain/373c3b27390417a56317781f515c6b11-2904268771383560871.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6a42f400-4c5a-4a9a-9482-92f4ad87ae0f', 'a5a13b2b-6e1e-40a4-b821-a5e175d2097c', 'IMAGE', 'https://cdn.chotot.com/Rk-PMo8foEFynHhuyjDRBra7FnjN5ynI_TTpvu6bOFY/preset:view/plain/acedfe20fd0eb5d97596b070a744b0eb-2904268771422160271.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('acc25f0a-f706-4fdc-84ed-a0e38bbcfb45', 'a5a13b2b-6e1e-40a4-b821-a5e175d2097c', 'IMAGE', 'https://cdn.chotot.com/R25bUMoShTfiQ1FOYu9LKi-A3P5oWOmdsJTfTs127-Y/preset:view/plain/e87a2d92d0cc1edc7cd87e54ea610a13-2904268772229622352.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('895c3689-82d9-41c9-8b59-9181360a3bbd', 'a5a13b2b-6e1e-40a4-b821-a5e175d2097c', 'IMAGE', 'https://cdn.chotot.com/njbnboqabvLOKnO5OzcdFzFzcAMNfdzFEoAjDDSWDkE/preset:view/plain/0e52172fefdf1e46f6f1e101856d0a6c-2904268772430931638.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1e455c5f-0982-4d9d-9699-a3d4d3e82ef8', 'a5a13b2b-6e1e-40a4-b821-a5e175d2097c', 'IMAGE', 'https://cdn.chotot.com/Jd1uqI0kryAwMpHbdt5viLra48s4nJpR50mtgTP4amo/preset:view/plain/2239392e8720a8151b5c6beb59e69fc3-2904268771516877071.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('56089d3c-58ed-4406-bc77-5850fbf16f44', 'a5a13b2b-6e1e-40a4-b821-a5e175d2097c', 'IMAGE', 'https://cdn.chotot.com/gzGgYGB5TxlwdPFxytaqKjANedS8Fl2MJBl1x5hJTkw/preset:view/plain/09afa9fe652115217ac9b523c94b1131-2904268771563910889.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('25f649b5-3a05-4e65-b813-b0884235e52f', 'a5a13b2b-6e1e-40a4-b821-a5e175d2097c', 'IMAGE', 'https://cdn.chotot.com/oQDIenTrVsEDwHRGpCncGsQrnxXmqtCKgdvhRgUJ_Lk/preset:view/plain/9a342999beafe479b60de7fe995beacb-2904268771649419207.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7d5daea7-a7d5-4c93-b52b-c9034844babc', 'a5a13b2b-6e1e-40a4-b821-a5e175d2097c', 'IMAGE', 'https://cdn.chotot.com/QD_nYSziwDvB5w30b_VymSOxtYHFOzIWrn4APbYKVo8/preset:view/plain/13601bd83d3a2993a9eadbb629cca633-2904268771610178271.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('550e8a8c-d3ff-4933-8d7a-73b07c7e41d2', 'a5a13b2b-6e1e-40a4-b821-a5e175d2097c', 'IMAGE', 'https://cdn.chotot.com/hvuXWu520cdmMgbWGInFW4F-Tzs-5fXZA_UpDhciv20/preset:view/plain/9f5c95f5470412616be3e38aaa45874c-2904268771534725586.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f7a56eae-55e6-4137-9a94-3dd74962e046', 'a5a13b2b-6e1e-40a4-b821-a5e175d2097c', 'IMAGE', 'https://cdn.chotot.com/3rprXdnWS3avchU-QOyAU2HUDo8gErh-4q8QEqj8A9I/preset:view/plain/ff776b3132a3b1f3a1f6a38f90f1709f-2904268771485641804.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d6076109-9d84-41e4-a63a-3cce49845414', 'a5a13b2b-6e1e-40a4-b821-a5e175d2097c', 'IMAGE', 'https://cdn.chotot.com/CUwwH7Hc1TDR-LDdmw8ppibAfNx8PyoKpDeChxNaguY/preset:view/plain/75b436cf0bf43c23ff82fe89632ba6a0-2904268771632284482.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('db364110-f300-4363-945e-a519fa1bd85a', 'a5a13b2b-6e1e-40a4-b821-a5e175d2097c', 'IMAGE', 'https://cdn.chotot.com/AcDmHuR0LwyO-X9KCs_-37B4sle58BdRe8YAbXUrfos/preset:view/plain/155263e6599f5f29cee5b818a8155d51-2904268772430960165.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('4bb41d7d-82db-413a-a3a3-6ec9576cddb4', 'P_133940293', 'APARTMENT', 'Bán căn hộ full nội thất chung cư Mizuki Park tháp MP5 view thoáng', 'Chỉ 3,48T có ngay căn full nội thất-mizuki park 
- Thiết kế: 2PN-1WC
- Diện tích 56m vuông
- Pháp lý sổ hồng
- Trang bị full nội thất còn mới, dọn vào ở ngay
- Tiện ích xung quanh: trường tiểu học NBK, siêu thị, ăn uống đông đúc
- Di chuyển Q1, Q4, Q7 các quận trung tâm 15 phút.
- View hướng thoáng ra Nguyễn Văn Linh, Quận 8', 'UNDER_OFFER', 'Huyện Bình Chánh, Tp Hồ Chí Minh', 56, 3480000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f7088524-af0c-48fd-9754-61854b643055', '4bb41d7d-82db-413a-a3a3-6ec9576cddb4', 'IMAGE', 'https://cdn.chotot.com/9yHnh_PTzx7CwrHjlw9YaRdn_Um_772NzT_zZLRLE8c/preset:view/plain/7bfe589b1a62c9717d667e5d268b89c8-2996120215078099863.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('97bb222b-ef4f-41da-aaf8-8ec6d740910a', '4bb41d7d-82db-413a-a3a3-6ec9576cddb4', 'IMAGE', 'https://cdn.chotot.com/dNwuYFKm4PFWyBmcfITyw60z2LRAeB05lBnOmUAEO-s/preset:view/plain/91d76c19d13427d9f4b7a1dc7fb37aca-2996120231016586135.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('814629c9-6029-4735-822c-df238e0e71b8', '4bb41d7d-82db-413a-a3a3-6ec9576cddb4', 'IMAGE', 'https://cdn.chotot.com/geJxhZ9h5zcf1Lzrn5BEMdstimbgQFZ-ZwRl91hOQoU/preset:view/plain/e8c9b95cb452b1983961ace83eb3508b-2996120254390483693.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7ba914a3-22ec-428a-bd81-894392d5306c', '4bb41d7d-82db-413a-a3a3-6ec9576cddb4', 'IMAGE', 'https://cdn.chotot.com/EDBxr4CZMf7nJkdojwMbjJCaE9LxU9nHsD-8w32qbqo/preset:view/plain/4164195b2e4f542b3c514a010a4327a2-2996120261755812589.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ebfe88f8-ee33-42a2-90f5-817cbd56dff1', '4bb41d7d-82db-413a-a3a3-6ec9576cddb4', 'IMAGE', 'https://cdn.chotot.com/rOUtrmqRL7F4vw6z7FgvJ6vFBhee09419S4qzZYD9Gk/preset:view/plain/55e3ea258103ca92a4e4562131ddcaf6-2996120286921898733.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('a7e857ba-593a-4435-81e4-8ddabfa00f3b', 'P_132809000', 'APARTMENT', 'Căn hộ mini 3.3triệu tuyệt đẹp 30m2:16/32 Tam Đông12, Thới Tam Thôn,HM', 'Cho thuê căn hộ mini mới 100% tuyệt đẹp tại :16/32 Tam Đông12, Thới Tam Thôn, Hóc môn
Diện tích sử dụng: 30m2 
Giá thuê: 3.3 - 3.5 triệu
Căn hộ nằm trong khu biệt lập, rộng rãi thoáng mát, nhiều cây xanh. 
Nhà xe rộng rãi.
Hẻm an ninh, rộng rãi
Miễn phí: 
Internet, xe, rác
Xem hình đăng thực tế
Liên hệ chính chủ: Ms Tuyết
', 'AVAILABLE', 'Huyện Hóc Môn, Tp Hồ Chí Minh', 30, 3300000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('20adc4d1-667a-4bc8-8c2b-ffcde6c01f5a', 'a7e857ba-593a-4435-81e4-8ddabfa00f3b', 'IMAGE', 'https://cdn.chotot.com/VjqVlYB2QMOX2LiN_TbFHBHBMWlHdW6EoiFKqvNIUmg/preset:view/plain/989c74368ac3669dc5250f069404f821-2987453046362511410.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('78734af5-312c-4e00-b1d6-07f886d92ca4', 'a7e857ba-593a-4435-81e4-8ddabfa00f3b', 'IMAGE', 'https://cdn.chotot.com/vcH3DsjDaCZL_zJNYYvsea7e7L5Od4T2S7Wy3dNLdyk/preset:view/plain/88dc78548a656fe7de30699d6d97c692-2987453146411970712.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cd0ca26c-ff69-4e1d-93c3-13eaf6748e79', 'a7e857ba-593a-4435-81e4-8ddabfa00f3b', 'IMAGE', 'https://cdn.chotot.com/utefhr3TYmtd_33T2Q76VCne37aGZoNaAIhE5bbo9ew/preset:view/plain/81a97b7d9244853cc84b97d07e21bd4d-2987453146154953846.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('412bdbb5-880f-4a55-afe5-64dda12307cd', 'a7e857ba-593a-4435-81e4-8ddabfa00f3b', 'IMAGE', 'https://cdn.chotot.com/TsiGWW3Q2_t4LWeygCJAbwMJiEknupxGurpgErUWcow/preset:view/plain/a19ae824c073038f3c10f7417ac263db-2987453146459882173.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('08159cf4-0d53-4e5a-81ee-926ab9db677f', 'a7e857ba-593a-4435-81e4-8ddabfa00f3b', 'IMAGE', 'https://cdn.chotot.com/xl1KUN1UL2ZOps1Tf73k4Hzq9v9Xsh7I0WCDI7mP3y4/preset:view/plain/76cd0f58d58e5c8d6d4364ad729b39a8-2987453147385420001.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('00714ca0-8640-4ec3-a356-08767070d476', 'a7e857ba-593a-4435-81e4-8ddabfa00f3b', 'IMAGE', 'https://cdn.chotot.com/OrxMK8isgNwvlrKNsnhPcdxQ6f338Nu7zSO4MTTgvFs/preset:view/plain/dbd829ac4bdba04ca199696ece1fbb45-2987453146915246374.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7eac3fae-88be-4957-ad9e-9989f6f6d37b', 'a7e857ba-593a-4435-81e4-8ddabfa00f3b', 'IMAGE', 'https://cdn.chotot.com/-jATKGaXmj6h7NMaR35ZKaKB4R23CNitU0SvCNIGyyE/preset:view/plain/312f58f8dcf87bc707b1f00eb0d1a51f-2987453239792517821.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cf7c9716-1dd3-4b07-a18e-d976432c73f1', 'a7e857ba-593a-4435-81e4-8ddabfa00f3b', 'IMAGE', 'https://cdn.chotot.com/K-ureqaECuRMJjmaayI6QV3zOqvgvCLbUKV4zamD-68/preset:view/plain/63dcdeb97f16c5302420ff1be0a190ef-2987453239686002157.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5b7801e3-7c7d-4c5a-b66a-db55092306ae', 'a7e857ba-593a-4435-81e4-8ddabfa00f3b', 'IMAGE', 'https://cdn.chotot.com/pfXyseJXziiR9RJR8xJhZX3mS5MCOvDIwSv2EfvFbpY/preset:view/plain/a22e26cb1c59e3e28503d48c0d7f0663-2987453239553354447.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6124423a-977f-43b4-8e83-e7c2b4e54dff', 'a7e857ba-593a-4435-81e4-8ddabfa00f3b', 'IMAGE', 'https://cdn.chotot.com/4ho7Q2z1W9z1wCMdKx6OtR6nH6u86fRzpZzBHzynW7A/preset:view/plain/3be15faf6e1322f31c954217290e3209-2987453240022548346.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e1802827-9d46-43ed-9059-65822059fd26', 'a7e857ba-593a-4435-81e4-8ddabfa00f3b', 'IMAGE', 'https://cdn.chotot.com/OwxViO1KSZwVVGVfWf-Dsz31dEaxS0tub6ybfkOghHk/preset:view/plain/aa3189c73c9622b088556bcc3046de8d-2987453239669550433.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('17c7c063-5e25-41a4-ac6d-2380c1f965e1', 'a7e857ba-593a-4435-81e4-8ddabfa00f3b', 'IMAGE', 'https://cdn.chotot.com/YQkJmu8shh10bJoz5WBKMplGdBut58lzo_4BQ1TWDiY/preset:view/plain/92e554a95cce1e2394683700b0f224c0-2987454635657675453.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('e9e74b76-b636-4b2b-9640-a49fa124f074', 'P_133940279', 'APARTMENT', 'CĂN HỘ MINI NGAY ĐẠI HỌC VĂN LANG CƠ SỞ GIÁ HỌC SINH SINH VIÊN', 'Dự án: 
Thông tin chi tiết: NHÀ ĐI BỘ ĐI QUA VLU LUÔN NÈ
Có thang máy 
Giừo giấc tự do 
Không chung chủ
Full nội thất 
An ninhhhhhh', 'AVAILABLE', 'Quận Gò Vấp, Tp Hồ Chí Minh', 35, 4450000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('db925992-265f-4452-8c23-b46aa97dd923', 'e9e74b76-b636-4b2b-9640-a49fa124f074', 'IMAGE', 'https://cdn.chotot.com/1_0o4Epy5LZNBZDO5F9i0VYdtBkPa6JqdfKk9Fe3MQU/preset:view/plain/495522aeda76494aabde83d70f81cbd6-2996120460660787577.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c1e1799c-cf42-4ff0-a237-39fe80d2dcfb', 'e9e74b76-b636-4b2b-9640-a49fa124f074', 'IMAGE', 'https://cdn.chotot.com/YYUz6p-JRW3JFoE7FLt-oeOY5DxSMvct8ikyMCs8k3c/preset:view/plain/e695088dfcd7658fcc1e6e2b431c6ee1-2996120460750332964.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ec52cdf5-1fd5-4939-a353-ef835c1758cc', 'e9e74b76-b636-4b2b-9640-a49fa124f074', 'IMAGE', 'https://cdn.chotot.com/Yn_F3R2xZN4UXzffu9WSCn740paoDCbBDba1ugsOEkU/preset:view/plain/b4b7696c5e6efbb71a2ea83946d3b30f-2996120461148410427.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a918551d-a5d1-489c-909d-b14e9acdf387', 'e9e74b76-b636-4b2b-9640-a49fa124f074', 'IMAGE', 'https://cdn.chotot.com/JixNgFesRgORGbkQEPORe9rg0vJ6ECzxceJ5E5qtGo0/preset:view/plain/08be622fa6292b790f1c1502223531e7-2996120460745389407.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('768fc912-e715-4c13-a25f-c340c3203e49', 'e9e74b76-b636-4b2b-9640-a49fa124f074', 'IMAGE', 'https://cdn.chotot.com/2AnOPAvttCwV-jQEB0M_mpjR2d71Zrnt1LAvx86lf9M/preset:view/plain/93b5eac64536b5a464f5152fbdceb19c-2996120461198339944.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6cc186ec-1265-4f07-adc6-228010df9df4', 'e9e74b76-b636-4b2b-9640-a49fa124f074', 'IMAGE', 'https://cdn.chotot.com/wlOEj83TX6u81tmXddH9UtShuWioFUbVU-p8RPql5ZE/preset:view/plain/a7426fcc6904bf7f83f374e5d00f7bcd-2996120460948776815.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6d47a84b-9528-482d-9360-338c5136b48c', 'e9e74b76-b636-4b2b-9640-a49fa124f074', 'IMAGE', 'https://cdn.chotot.com/-Rs2EJuvxl8a6u79bDmzIC4hJU5bsgGWCS3fWzlUwxI/preset:view/plain/cc18b3a981041437bc7127eda278da7e-2996120460864999015.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9107027a-b500-4334-974f-e0dca3f5c859', 'e9e74b76-b636-4b2b-9640-a49fa124f074', 'IMAGE', 'https://cdn.chotot.com/H1SakOMMHiTYcyy1S01e8NNuq_LOLMXcgjExEPm-g5c/preset:view/plain/60f9cb0da9b59ce9054f87a4abb3d6bc-2996120460897065113.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3df376a9-d05c-49b0-9050-f8f22803f358', 'e9e74b76-b636-4b2b-9640-a49fa124f074', 'IMAGE', 'https://cdn.chotot.com/Vn2gJHvp5E315gK99G04t26m8GkgN_gx-6SeEvY2n6I/preset:view/plain/6f3f1a97cf4de75e5a785fe5d4f38fc6-2996120460930457688.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0fecf82c-cbba-4636-aa3f-162e44ab813a', 'e9e74b76-b636-4b2b-9640-a49fa124f074', 'IMAGE', 'https://cdn.chotot.com/_vz_pGSNQiX2xQO60-Lor_vUWEld-StgxBDnaYZqBXA/preset:view/plain/b42202e2c7fd4fcbeb46666828fc8bf4-2996120461181571109.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c1181337-a017-4348-9b27-7871cc9d13fc', 'e9e74b76-b636-4b2b-9640-a49fa124f074', 'IMAGE', 'https://cdn.chotot.com/zBBceRHmzZMoplSVavIWekck-ay13u6nzEgwnWQ0KUY/preset:view/plain/92a9424e686d1e51fc1a9d0e50668f13-2996120460795682642.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('479362b7-9f49-44bf-9c8d-b28c472ac571', 'e9e74b76-b636-4b2b-9640-a49fa124f074', 'IMAGE', 'https://cdn.chotot.com/c56MPj9w4d4S9Jyv1OZPyItv8n4h0xIxnn-lPdzPwb8/preset:view/plain/d756b4c80842663e728481189d488cfa-2996120460882074519.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('fd263bbc-c3a3-49eb-b65b-3043ae0a4969', 'P_132749070', 'APARTMENT', 'Cho thuê căn hộ idico tân phú giá 9tr/Th- 60m2/2PN+2WC, Full nội thất', '- Diện tích: 60m2/2 phòng ngủ-, 2WC, phòng khách, bếp, ban công.

- Nhà đầy đủ nội thất.
- View đẹp thông thoáng.

- Ngay đầm sen tân phú sở hũu mọi tiện ích trong vài bước chân.

- Giá thuê: 9triệu/tháng.
- Liên hệ: ***', 'SOLD', 'Quận Tân Phú, Tp Hồ Chí Minh', 60, 9000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1edbf4b8-6b43-46bb-8ce5-0bb9d25ca2bd', 'fd263bbc-c3a3-49eb-b65b-3043ae0a4969', 'IMAGE', 'https://cdn.chotot.com/DVOaXd7YoZ8zUOwnaxrjwaHqYYyrktxmzvES-P9bHlw/preset:view/plain/a90350146917ae24f802b5a6cb6b71e4-2990069658225268563.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('652b7590-9a85-4ac2-b3ef-dc1492999e58', 'fd263bbc-c3a3-49eb-b65b-3043ae0a4969', 'IMAGE', 'https://cdn.chotot.com/XDtEk_0U56zwuUcuho6AMUfDRdUbqeFzS8uMSQZ0yYY/preset:view/plain/ddf06cab3595e0c6a26fa391e49821df-2990069657318222449.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ff3d601a-b4a8-49d3-ab5b-33507f91930a', 'fd263bbc-c3a3-49eb-b65b-3043ae0a4969', 'IMAGE', 'https://cdn.chotot.com/lmOcWR8kZ7cSrdROZTEBKJwt_xHlKkqzDX_OlwN2pnM/preset:view/plain/6d9be1390edba72fedb3424d86464ea7-2990069657414932344.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('10d1e7a3-c42b-4cd4-bc45-3a3b12ccd300', 'fd263bbc-c3a3-49eb-b65b-3043ae0a4969', 'IMAGE', 'https://cdn.chotot.com/SwkCG0Xun6zZVHeT_jNytZziXWLq3zCVoTEYvj_urrE/preset:view/plain/7591a1613b6c3cd928519dbbf6715a80-2990069657494262032.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('4ddc5360-f9a6-44f4-a79f-c3777a9ba245', 'P_133940262', 'APARTMENT', 'CĂN HỘ DỊCH VỤ CAO CẤP 2PN QUẬN 3 (NGAY CHỢ BÀN CỜ)', 'Dự án: 
Thông tin chi tiết: CHUYÊN CĂN HỘ DỊCH VỤ CÁC QUẬN 1, 3, 4, 5, 6, 7, 8, 10, BÌNH THẠNH, PHÚ NHUẬN, TÂN BÌNH
📍Địa chỉ: Cư xá Đô Thành, Quận 3
⭐️Tiện ích:
- Kết nối trực tiếp Điện Biên Phủ, Nguyễn Đình Chiểu, Cao Thắng, Lý Thái Tổ, 3 Tháng 2.
- Free toàn bộ chi phí dịch vụ, an ninh, bảo vệ 24/24, dọn dẹp, vệ sinh hàng ngày.
📞 Liên hệ em Quân
*** (Minh Quân)', 'SOLD', 'Quận 3, Tp Hồ Chí Minh', 83, 36000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('704bbac2-9bfa-4d99-a943-a16dcb43a36a', '4ddc5360-f9a6-44f4-a79f-c3777a9ba245', 'IMAGE', 'https://cdn.chotot.com/kltdEFG01BFI5znBnJi8u1E7B-T9w0EKxWtvkXvMBOw/preset:view/plain/56ada98fdea9ef5eaf7e1b0a9a9dda53-2996118730611451558.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2064bf8f-29c6-4f0a-86a8-96e158464ba8', '4ddc5360-f9a6-44f4-a79f-c3777a9ba245', 'IMAGE', 'https://cdn.chotot.com/NoWi5fw13Jbl2q-uTF8SDHDVE1vmGHklepcP1UtvERo/preset:view/plain/2d1fdd8c4ea4ca50ed402d10c3457027-2996118730930510413.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2077e261-9bae-4e14-aa9d-297e45cf50e6', '4ddc5360-f9a6-44f4-a79f-c3777a9ba245', 'IMAGE', 'https://cdn.chotot.com/CKWa3QjDfwAJJwqvLQ63JcZOCGjXaHTiNfPodOZjKrg/preset:view/plain/d1dd8ac452a2fbb8ac5904fac2e22c2f-2996118730927365015.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ec55006e-d6c2-42f9-8f9e-5ab6e8351991', '4ddc5360-f9a6-44f4-a79f-c3777a9ba245', 'IMAGE', 'https://cdn.chotot.com/KVQfrgV5mhmeBVj_OEQ2-u_50UCHaMRMJw7XRLlg_I0/preset:view/plain/84814715d629b3fe239d6c3debe34e13-2996118730060190719.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ba01306f-e0fe-49de-acf5-15f11d366dee', '4ddc5360-f9a6-44f4-a79f-c3777a9ba245', 'IMAGE', 'https://cdn.chotot.com/4PEXHDQIbRCRMfEVIXKgL_8LPdswEMTNKwEzQg1rGYc/preset:view/plain/a2e58027a7255314c62017e696b04a37-2996118731081538710.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('697a6af9-a65b-40f9-b1cc-fd21af34843c', '4ddc5360-f9a6-44f4-a79f-c3777a9ba245', 'IMAGE', 'https://cdn.chotot.com/2IYB1JMKoEbhysVst3sTYcsjuChfwSpvpyvM7TccuGc/preset:view/plain/7f623bf951a24034ec1055f01aaf6352-2996118730435272792.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8a59cf3a-87aa-46f8-8d85-813a6a0dd96e', '4ddc5360-f9a6-44f4-a79f-c3777a9ba245', 'IMAGE', 'https://cdn.chotot.com/PTlcEIV9qEXAi2y_ak1ixKv317Xq-X8PRvdxgKw0jlM/preset:view/plain/bd71feeabdf02073a92de13c94645bfc-2996118730913780856.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a185cc9f-7591-45a7-b660-ef3a249c1702', '4ddc5360-f9a6-44f4-a79f-c3777a9ba245', 'IMAGE', 'https://cdn.chotot.com/-4Xpfz2K9vNi3ZzB9l6TdWjMY0HQ9swhYEO_QgzcxJ8/preset:view/plain/98c57c1ccef201f9229d77e030619901-2996118731031919341.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7d73fe24-5770-4e4c-bf00-932c0e7a1a0f', '4ddc5360-f9a6-44f4-a79f-c3777a9ba245', 'IMAGE', 'https://cdn.chotot.com/3-3PzdKwMNb9x2GGUp68SRNRKeYNwV8U1I3XGz4bFKo/preset:view/plain/6c0e6476a293e405eceb26ad966f7fd9-2996118730964099943.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('605147a1-8a66-4d08-ad62-ff209d066161', '4ddc5360-f9a6-44f4-a79f-c3777a9ba245', 'IMAGE', 'https://cdn.chotot.com/nih-qdhHzvl8dX_4GTp08xPaYY2dJiV9piGYhQbwmdg/preset:view/plain/80d9cbd97c207312547c96fe2f548824-2996118730423769169.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('90bc1b56-fa38-4b02-b00e-c886b4f16dee', 'P_129003120', 'APARTMENT', 'Cho Thuê Studio Full NT Free Hồ Bơi + Gym Nhà Đẹp Ở Ngay', '⭐️Cho Thuê Studio Full Nội Thất Đối Diện Lovera Vista Có Hồ Bơi + Gym🌟

✅ Bảo mật 3 lớp khoán vân tay, thẻ từ mật khẩu
✅ View mát mẻ thoải mái, thiết kế view đón nắng ấm
✅ Khu An ninh 24/24
✅ Nội thất bao gồm
➡️ Máy lạnh, quạt trần, Hút Mùi, Tủ lạnh, máy nóng lạnh, Máy Giặt, Máy Xáy 
➡️ Giường, nệm, tủ quần áo
➡️ Sofa, bàn ăn
➡️ Sân phơi, Sân chill view ngắm nhìn toàn cảnh Phong Phú 4
Giá : 4.000.000 
-------------------------------------', 'AVAILABLE', 'Huyện Bình Chánh, Tp Hồ Chí Minh', 35, 4000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c122bf48-c763-476e-bfc8-9a3800e9e29a', '90bc1b56-fa38-4b02-b00e-c886b4f16dee', 'IMAGE', 'https://cdn.chotot.com/zNVs-2GW1oG-KxkuMDIFd1-cxp_qfpbyU37qJHuHJWo/preset:view/plain/903784f3754c3046a9171db0359e2d87-2957572652366269740.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('71950a98-a864-4555-b8cd-079ff5a2a3d3', '90bc1b56-fa38-4b02-b00e-c886b4f16dee', 'IMAGE', 'https://cdn.chotot.com/c_p1_xP51-dGmFdGLKF9bXbAajSXU5c3Hnn0Grz4VQ4/preset:view/plain/4caed026f4f939d5eafd51d8f5a7098a-2957572652319525371.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3ecc8f36-cde1-4453-9c21-2792ddcbbd6d', '90bc1b56-fa38-4b02-b00e-c886b4f16dee', 'IMAGE', 'https://cdn.chotot.com/zj5E5yYs2ZVNiJRNdoNVgaRCD_VoNBu-a_oO14qgwRU/preset:view/plain/e521009a96f9641d71e771f26efd5e41-2957572652141528740.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1e4217d5-4450-4092-a9cc-7b4cdfa138d6', '90bc1b56-fa38-4b02-b00e-c886b4f16dee', 'IMAGE', 'https://cdn.chotot.com/Wi28acsyEAsQu56-MrpdIY_Buiyj1kk47mIWjPlyqmE/preset:view/plain/0aaefdd2f4e1c8492647510593d00ab3-2957572651328078838.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f27298e4-355a-4f94-b0c0-18750ebabb78', '90bc1b56-fa38-4b02-b00e-c886b4f16dee', 'IMAGE', 'https://cdn.chotot.com/cb6gE55CSxoBArKqI28bYFNtzAJu0OAstDqakwtggLQ/preset:view/plain/288e5d04349117845d8d9971af580073-2957572651308564544.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b86d06bc-c9a3-4f1f-9035-80a38e245cb7', '90bc1b56-fa38-4b02-b00e-c886b4f16dee', 'IMAGE', 'https://cdn.chotot.com/J8XQNd8cI1hyenUslTCof381QBuFRLxVUpsCA7TgazI/preset:view/plain/68410070a040bf7b2d59ff31f41cb946-2957572652407776460.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e7a663a3-b5f0-4b38-bc98-f3f4efffeef9', '90bc1b56-fa38-4b02-b00e-c886b4f16dee', 'IMAGE', 'https://cdn.chotot.com/Sjw0KQBopB662lakeFfZVZ3yzaI3TQ-a7tloxioxypE/preset:view/plain/b54f45232cbbd7e15cccf57d20f82674-2957572651911982647.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('04b457bd-2065-4061-939d-014bdae16223', '90bc1b56-fa38-4b02-b00e-c886b4f16dee', 'IMAGE', 'https://cdn.chotot.com/eSROcXyeh08ecoJiDkFiwGAoqtSYQVkrvwLGajffWmE/preset:view/plain/dc14b170494198bf19819ed5e5c48022-2957572652443944927.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4103a94a-2077-4c3a-8b66-31f012db12b1', '90bc1b56-fa38-4b02-b00e-c886b4f16dee', 'IMAGE', 'https://cdn.chotot.com/BQoCqA3PUZE2zXVE2FDifY0ky0u7dJU2FW2lWbB0vuY/preset:view/plain/dbdaa6684a8f1ae59fced24249cf1cc3-2957572652391830665.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0f1c62a6-df44-40d5-a8c6-221fc7e1a4b3', '90bc1b56-fa38-4b02-b00e-c886b4f16dee', 'IMAGE', 'https://cdn.chotot.com/usAxWlL47PKFqLdR2jkftGaGkd74Z0dTixW5smqbXiM/preset:view/plain/1d9e9e8ed43f6c62af753abfadcb581c-2957572652523104908.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a2975819-09a1-41e9-8662-9b45f6f31884', '90bc1b56-fa38-4b02-b00e-c886b4f16dee', 'IMAGE', 'https://cdn.chotot.com/xS3XtPEBJ1LIBFhPVs8wRwQuekOub8-zXdP-Zh-rjkk/preset:view/plain/3e50d0dd7285f06eaaccaf86850321f2-2957572652456503683.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5ea983c2-2b2e-4de6-a49e-8208819aaa4f', '90bc1b56-fa38-4b02-b00e-c886b4f16dee', 'IMAGE', 'https://cdn.chotot.com/NOM_UauH_zVgVuRbGnhFMIR8-zKPTdDZ1fhYlJLa7J4/preset:view/plain/e9bf52d6964f57453f18786272075211-2957572652242291960.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('b0e09b49-6bd3-41cc-a8fd-29e663627bf7', 'P_133913767', 'APARTMENT', 'BÁN CHUNG CƯ ĐƯỜNG HÒA HƯNG, QUẬN 10 - 68M2 - 2PN  - GIÁ 2.85 TỶ', 'Diện tích: 68m²

Kết cấu: 2 phòng ngủ, 2 phòng vệ sinh, thiết kế tối ưu công năng, không gian sinh hoạt chung rộng rãi.

Giá bán: 2.85 tỷ (Mức giá cực tốt tại khu vực trung tâm).

Ưu Điểm Nổi Bật
Vị trí trung tâm: Tọa lạc trên trục đường Hòa Hưng, kết nối nhanh chóng sang Quận 1, Quận 3, Quận 5 và Tân Bình. Giao thông thuận tiện, không lo kẹt xe lớn.

Tiện ích ngập tràn: Vị trí cực kỳ thuận lợi cho gia đình có con nhỏ đi học với hệ thống trường học các cấp xung quanh. Gần chợ, siêu thị, bệnh viện và các tiện ích thiết yếu khác.

Tiềm năng lớn: Căn hộ 2 phòng ngủ 2 vệ sinh hiếm có trong tầm giá dưới 3 tỷ khu vực trung tâm, phù hợp để an cư lâu dài hoặc đầu tư cho thuê sinh lời cao.

Liên Hệ Xem Nhà
Họ và tên / SĐT: ***

Hỗ trợ xem nhà thực tế, pháp lý rõ ràng, sổ hồng chính chủ giao dịch nhanh.', 'AVAILABLE', 'Quận 5, Tp Hồ Chí Minh', 68, 2850000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dab84cd7-d583-4537-b60f-f137b140b976', 'b0e09b49-6bd3-41cc-a8fd-29e663627bf7', 'IMAGE', 'https://cdn.chotot.com/yj9gDxcet7IZnW4IoNwoTM1THaDLVyHbp6dAuD8UTJg/preset:view/plain/d5283ee724207e40766cef2200378d83-2995947322269745749.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('808d5a9b-5edc-4442-861f-43d17fd17adb', 'b0e09b49-6bd3-41cc-a8fd-29e663627bf7', 'IMAGE', 'https://cdn.chotot.com/40lNpwOETqO0dSidtNnSQrK8xLCGA3kJZz-oumcXTy4/preset:view/plain/5835ce4e8ccdd2f06f07a61fd35da5e6-2995947261216473685.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('65d76a93-5dbb-41cc-be6d-113339e243a1', 'b0e09b49-6bd3-41cc-a8fd-29e663627bf7', 'IMAGE', 'https://cdn.chotot.com/CVxnZcFLpBPzzS6sBe7gklRO0kg3rJyZNLCJkK5Ucq8/preset:view/plain/defe0314133c355d4cd24281c60fdcfd-2995947261364192740.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b860af70-64b7-49ef-937b-ad128ea2532f', 'b0e09b49-6bd3-41cc-a8fd-29e663627bf7', 'IMAGE', 'https://cdn.chotot.com/xWSoYNQUzrl8MNmwyJsNLTDuWJsySOtp3rdjUBejZmI/preset:view/plain/332b7d6e81ae146e5ae7acf7afede9db-2995947261333490041.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('67a8957b-c795-418b-aa19-c6f08cae5827', 'b0e09b49-6bd3-41cc-a8fd-29e663627bf7', 'IMAGE', 'https://cdn.chotot.com/sc4QId5fryPPHffE_Ap7tSzRdb4Ph967gstm_C2ImbI/preset:view/plain/58f21e0dfecc3c2d04ba3745003dccbc-2995947261360081492.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2f80322f-54ae-4275-8f6e-593c5eac10bf', 'b0e09b49-6bd3-41cc-a8fd-29e663627bf7', 'IMAGE', 'https://cdn.chotot.com/7b5bMML7mHLw5ddO5chZi7Ig-xIgROmtTC61AIWqv9c/preset:view/plain/efb2405e832f71eee22668c611447cd6-2995947261379694567.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1453c697-6d6b-47ca-b0ad-2f5703ce09da', 'b0e09b49-6bd3-41cc-a8fd-29e663627bf7', 'IMAGE', 'https://cdn.chotot.com/liWzTdGdAQfml3_xIVL141NGQwDQIjLLPQDQb2QYFsA/preset:view/plain/d54ecd1d46329e6d2cfb39d88ea837e2-2995947262584883796.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('db93d6b5-7c1b-47a8-8e0f-2f1749bd9f04', 'P_133263114', 'APARTMENT', 'Căn hộ Dv 30m2 Full nội thất cao cấp(lầu 2) MT đường Võ Oanh,P25,BT.', '* Cho thuê căn hộ Full nội thất cao cấp dt: 30m2 ( lầu 2 ) tại 72 Võ Oanh , P25 , Bình Thạnh 
- dt căn hộ 30m2 Full nội thất gồm : tivi 40in + tủ lạnh + máy lạnh + máy giặt + bếp từ + lò vi sóng + bàn làm việc + bàn ăn + Gế bành thư giãn + giường chăn ga gối + tủ quần áo + quạt trần + Sen tắm nóng lạnh…
- giờ giấc tự do, an ninh khoá vân tay
- tiện ích quanh nhà thuê : bước xuống nhà ngay phố ẩm thực , không thiếu thứ gì, giáp 5trường đại học Huter , GTVT, Ngoại Thương, Hồng Bàng… công viên sau nhà thuê, bến xe buýt cách 100m Ga metro, di chuyển Q1 5’p…
- giá thuê: 8,5tr/th
Các phí khác:
Điện : 3,8ngàn /kw 
Nước: 150ngàn/người
Dịch vụ (gồm: wifi + rác + vsinh cầu thang):  200ngàn/1phòng
Xe máy để fee : 2xe

- Nuôi pet xin trước có cam kết 
- Bãi xe tầng trệt
- Thang bộ 
- Không nhận em bé , người nước ngoài', 'AVAILABLE', 'Quận Bình Thạnh, Tp Hồ Chí Minh', 30, 8500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bc22f49a-7d94-4f6d-bd08-42deffd2b244', 'db93d6b5-7c1b-47a8-8e0f-2f1749bd9f04', 'IMAGE', 'https://cdn.chotot.com/Xwi9UbrrkVqKQwaQPRZa2yT3wCd2ETxb5y-Db9NU6ro/preset:view/plain/a7df347df4ddbfb8e2dc1b745c150176-2995079879938003605.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4a2e577a-d78c-49dd-8304-1f0f317fa0c5', 'db93d6b5-7c1b-47a8-8e0f-2f1749bd9f04', 'IMAGE', 'https://cdn.chotot.com/oBHEv6qoq1k7zDIM1JB5MDum0HKWiWB5oDRI-TBEQls/preset:view/plain/5619c41925066424513ec2f47033ae5e-2995079879642496500.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d78acd99-b3e5-422c-bc05-9a51c0e41145', 'db93d6b5-7c1b-47a8-8e0f-2f1749bd9f04', 'IMAGE', 'https://cdn.chotot.com/aKDhCemHXlayVToINhgLlhf7Fcz3V8e7ReL03BskwCU/preset:view/plain/587b55006a9f1b9089ec8f9cdb2a1f32-2995079879687110651.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6bb8a6d9-3a59-41b7-81fc-30067681e50b', 'db93d6b5-7c1b-47a8-8e0f-2f1749bd9f04', 'IMAGE', 'https://cdn.chotot.com/DFd5YwY78YYzCmBFgaMVdv_QKifD8dnviipWUN0aDkg/preset:view/plain/6602a23187cf180bbfc56bd6e5be2f5f-2995079879189420051.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c63f1b6b-984a-4c48-8e5b-d7cc4c337adc', 'db93d6b5-7c1b-47a8-8e0f-2f1749bd9f04', 'IMAGE', 'https://cdn.chotot.com/LqwCuah4T0KaElaMUu6Mt5FlmNSHs7jjdoLzVC8SNHw/preset:view/plain/f70012a0706e22b4553974acfba0054e-2995079879218751745.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4a9558dd-a3ae-4cdc-b45c-4a7c12e0a79b', 'db93d6b5-7c1b-47a8-8e0f-2f1749bd9f04', 'IMAGE', 'https://cdn.chotot.com/tVo-rxfPx_3D298LHalzGLQquT062Bu1FXwqSWZwxjg/preset:view/plain/f29f83c0ac2c0ec557e5d9f183e82411-2995079878652637396.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('41e3e43b-5753-4c44-bdb9-3bc113548ced', 'db93d6b5-7c1b-47a8-8e0f-2f1749bd9f04', 'IMAGE', 'https://cdn.chotot.com/Py-chYtUFdYjfA-wxJqc3w-RtVV0jR5Jk1zNPNWERMw/preset:view/plain/b88b708b4c483d52e5f01b8f5221f790-2995079880035303432.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4d1cf3f4-598f-4750-87ce-e4c227049835', 'db93d6b5-7c1b-47a8-8e0f-2f1749bd9f04', 'IMAGE', 'https://cdn.chotot.com/qf98mxKfhMYHBWSG6mv5yW6yQzYP08p45B43Ey9VetU/preset:view/plain/e25c101e1103253f5a68fded509fe7d1-2995079872700442613.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('78b511fc-dc54-44f8-a6d9-1f604a17d4e7', 'db93d6b5-7c1b-47a8-8e0f-2f1749bd9f04', 'IMAGE', 'https://cdn.chotot.com/JeX_K7HjPNHy5-RCm4oqtmrFFXoSv3-jeryYiV0JHiA/preset:view/plain/5314342d2ee18aaa90acd757a8d77020-2995079872807801362.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c2efe109-5e9c-4bbe-bbc5-0fb69cc509a4', 'db93d6b5-7c1b-47a8-8e0f-2f1749bd9f04', 'IMAGE', 'https://cdn.chotot.com/-FTciwNzHCD51jUkmhW8gEYB46fQF_WO2lyTtpgJWO8/preset:view/plain/b1b5a84da7dfea442c904a94c606e454-2995079873401308780.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2071a571-a0d6-4283-81f5-685b7aa48e71', 'db93d6b5-7c1b-47a8-8e0f-2f1749bd9f04', 'IMAGE', 'https://cdn.chotot.com/JwRI9ZDjvAxYTG6VG387THsPTtCMaxpevrxrovnZhns/preset:view/plain/645514075b1dbe40dffda3eb17170757-2995079872958742913.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('429cb397-5adf-46bd-a8e5-d25d33da8b92', 'db93d6b5-7c1b-47a8-8e0f-2f1749bd9f04', 'IMAGE', 'https://cdn.chotot.com/5bAj9nuFSUqPEVMNho0-HcfqXkwp_EpsGRTMBjewt4A/preset:view/plain/041544bec6280e90b5f5d53901d1f198-2995079873418078011.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('13abd4c1-2b48-4b0a-9ba6-803a614027e9', 'P_133940233', 'APARTMENT', 'Siêu Phẩm 2PN FULL Nội Thất Cao Cấp Xịn Xò Sắp Trống!!!', 'Dự án: 
Thông tin chi tiết: 🏡 Bình Thạnh, Phú Nhuận, Gò Vấp, Quận 1-3

🪴 Căn góc ban công – Tràn ngập ánh sáng, đón gió cả ngày

🛋 Full nội thất mới toanh – Chỉ cần xách vali vào là ở ngay

🔐 Khoá vân tay + Camera an ninh – An toàn tuyệt đối 24/7

🚪 Không chung chủ – Tự do sinh hoạt, riêng tư 
-------------------------------------------------------
💰Giá thuê: 1PN 7.5-12 triệu / 2PN 9-15 triệu
💰Giá thuê: Studio 6-9 triệu / Duplex 6-8 triệu', 'AVAILABLE', 'Quận Bình Thạnh, Tp Hồ Chí Minh', 60, 12000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('725f781f-4715-4e93-b8ec-7974a4041c76', '13abd4c1-2b48-4b0a-9ba6-803a614027e9', 'IMAGE', 'https://cdn.chotot.com/A7GpubOg9ohowiDPik0Xd7rkjKOuEOg06vmwG21095k/preset:view/plain/176bb6c7600546e06d6d78801e98fdc7-2996120304286710509.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7d158fab-6585-4ddc-a69b-13bf62e49bd5', '13abd4c1-2b48-4b0a-9ba6-803a614027e9', 'IMAGE', 'https://cdn.chotot.com/qSfbxdwTFwm1pkSqQ9TJzZnE2k9X0KIq-3N0g2wC3vs/preset:view/plain/527b57d92f0c4997cf519c43929b89a2-2996120304200295460.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fa533a40-4243-4b09-a044-12542a55b543', '13abd4c1-2b48-4b0a-9ba6-803a614027e9', 'IMAGE', 'https://cdn.chotot.com/JErl6uMBRoxMgdggFZxnEgR8c73p3GNDcrkpP6kTqi0/preset:view/plain/4cd95d009f07925333118d3f7f20e84f-2996120304098133476.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d1fb1cd5-f15e-4f43-b95b-e9573012eeb8', '13abd4c1-2b48-4b0a-9ba6-803a614027e9', 'IMAGE', 'https://cdn.chotot.com/NjyDnW7jC5MOJ9MsAxIUQ78_2iiG6igfoVopuJP0TD0/preset:view/plain/9a5a4aeeb325a8a86e0bb162781c5ca6-2996120304431669336.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ee40d2c9-349c-49ad-b9d8-8d79012b9d6b', '13abd4c1-2b48-4b0a-9ba6-803a614027e9', 'IMAGE', 'https://cdn.chotot.com/gXE0wR8BC4XhngpXhuE3rcEFBTLDEUmoV1Zx3KmOY1k/preset:view/plain/5b132365ae2a93d77dfc331dc74981c4-2996120304381958297.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5810618a-e4cc-432b-8ca3-cd5ac448bf4d', '13abd4c1-2b48-4b0a-9ba6-803a614027e9', 'IMAGE', 'https://cdn.chotot.com/_AIzNO_lwOAN1qaPrgj1MUbx8FYQqwRPoLMbujaodOU/preset:view/plain/431c8c7c9ccbc1d0ad9187b96d6e596f-2996120304459437055.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('082f2a11-2de4-4387-bf4c-faf2917e5b6e', '13abd4c1-2b48-4b0a-9ba6-803a614027e9', 'IMAGE', 'https://cdn.chotot.com/drovEj9iyQEH9UNmu6hWIO9HoW-uSufGanfbIQYuYBE/preset:view/plain/c3475d4b3f2a6e607888bc7478e55e14-2996120304297922151.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('180c4693-8482-4b0f-9f4c-442c9b20a288', '13abd4c1-2b48-4b0a-9ba6-803a614027e9', 'IMAGE', 'https://cdn.chotot.com/RGSF_dNh8iloi5hH_WB-_8tAkgZq8ULRItGROis8oqs/preset:view/plain/7007480c9011d081b8b74a1f15c6cde7-2996120304261286265.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d619e84e-c59e-4a97-b157-43ef9cd5b181', '13abd4c1-2b48-4b0a-9ba6-803a614027e9', 'IMAGE', 'https://cdn.chotot.com/WmhTRRTi0jERGWVTIglWwGyUgSWK2XrDzVGNc1KN_yA/preset:view/plain/c04f75be46bff3c762c3aa5500468e25-2996120304450377809.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('71510b9e-bf9a-4056-b6e2-d417fa2fec5a', '13abd4c1-2b48-4b0a-9ba6-803a614027e9', 'IMAGE', 'https://cdn.chotot.com/tBq35XemCkEPusAG5MR1oIgqPBGD6QOof20tEkbcuMs/preset:view/plain/f35b2d43ed458519061d68e8c47ea80b-2996120304382934541.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('758ebd62-386a-4c20-8282-3de473382be9', '13abd4c1-2b48-4b0a-9ba6-803a614027e9', 'IMAGE', 'https://cdn.chotot.com/P3sqKWuNz1f08WZ9krYZ-Bs3lJBRcIew0LLR3OWEzEc/preset:view/plain/d18bbfdcb73ad500020d459686226977-2996120305541039588.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b94e89b5-90c6-47a6-a5fb-9e51bf8d8265', '13abd4c1-2b48-4b0a-9ba6-803a614027e9', 'IMAGE', 'https://cdn.chotot.com/h_QZUNtkL39cuarG-AYZif5kNne9nPMEIje-eQx_IMo/preset:view/plain/d18beba0d3dac40b01cad071daaa1916-2996120304417138342.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('165befba-be55-43a6-836a-394138fc162b', 'P_133696072', 'APARTMENT', 'Cho thuê ICON 56 căn 3pn 2wc không nội thất chỉ 18tr/th, rẻ nhất Q4', 'Dự án: 
Thông tin chi tiết: Kim chuyên cho thue ICON56 quận 4 *** zalo whatsapp', 'AVAILABLE', 'Quận 4, Tp Hồ Chí Minh', 97, 18000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('81abfc55-8581-4442-b9fe-e7a0e1514d41', '165befba-be55-43a6-836a-394138fc162b', 'IMAGE', 'https://cdn.chotot.com/BAsvPy4tqmWRaWnI9UHdOr6HptUZnDu0quq4ma49KaY/preset:view/plain/87aaf60768f6d1980c261d2b99db1c11-2994248343686473640.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2e2757f3-9097-4b15-95c3-22d191476879', '165befba-be55-43a6-836a-394138fc162b', 'IMAGE', 'https://cdn.chotot.com/i11j86X6ObhDwjhNp3ukw8H0nIMwXfb74CEvkdSPUv0/preset:view/plain/d928de4f99e8bf4c0c83aafd0039db32-2994248343648335848.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('65c2517c-478c-4dbb-b5c0-add03e61ae14', '165befba-be55-43a6-836a-394138fc162b', 'IMAGE', 'https://cdn.chotot.com/0IVjB5PgP8BGhtLIvopBlq0riMg2Z1qRnDsOBRiEjqI/preset:view/plain/8a16347012331e785865671f350b3cfa-2994248344577290130.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('b11fe45b-0c2c-4551-9a01-d6206ebe9b00', 'P_133940228', 'APARTMENT', 'CHO THUÊ CHUNG CƯ CỘNG HÒA PLAZA, TÂN BÌNH - 100M2 - 3PN - GIÁ 17.5 TR', 'Diện tích: 100m² (Không gian rộng rãi, thiết kế thông thoáng).

Kết cấu: 3 phòng ngủ, 2 phòng vệ sinh, phòng khách và bếp rộng rãi, thích hợp ở gia đình hoặc làm văn phòng.

Giá cho thuê: 17.5 triệu/tháng.

Ưu Điểm Nổi Bật
Vị trí vàng: Tọa lạc ngay mặt tiền đường Cộng Hòa, quận Tân Bình, thuận tiện di chuyển sang Phú Nhuận, Quận 3, Quận 1 và chỉ vài phút ra sân bay Tân Sơn Nhất.

Tiện ích giáo dục: Nằm gần nhiều trường đại học lớn, rất thuận tiện cho sinh viên, giảng viên hoặc gia đình có con em đang học tập tại khu vực trung tâm.

Tiện ích đẳng cấp: Tòa nhà tích hợp đầy đủ siêu thị, trung tâm thương mại, phòng gym, cà phê, an ninh bảo vệ 24/7, thang máy thẻ từ an toàn.

Liên Hệ Xem Nhà
Họ và tên / SĐT: ***

Hỗ trợ xem nhà nhanh chóng, thương lượng trực tiếp chính chủ, nhận nhà ngay.', 'UNDER_OFFER', 'Quận Tân Bình, Tp Hồ Chí Minh', 100, 17500000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a382c86d-1a8f-42d2-84bc-d600ddcdbde8', 'b11fe45b-0c2c-4551-9a01-d6206ebe9b00', 'IMAGE', 'https://cdn.chotot.com/xSvCQTPVMK1S9FpTVETOOalf_xCiXjVCLYz2-r82jgI/preset:view/plain/22ece08f705453c3277ddc6ada059802-2996119648257480785.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('209b5d38-1848-4f0c-8c9b-34585ef9a841', 'b11fe45b-0c2c-4551-9a01-d6206ebe9b00', 'IMAGE', 'https://cdn.chotot.com/FR6Z45wZRh1kO25p9MdKl-DwtvHogsm0U_yywo3pfhM/preset:view/plain/00c44162b208725382ac1b3f2858eab5-2996119647956097943.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('681895a5-cd51-4db1-8a39-493a95a10574', 'b11fe45b-0c2c-4551-9a01-d6206ebe9b00', 'IMAGE', 'https://cdn.chotot.com/-0QLzqscvgg5HoxpqwDjPmj1FdZ_yXndweuGLAdDeNI/preset:view/plain/00c18a82a336e62ec740a15f898374fe-2996119647803709593.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e4440be2-92b5-4a72-8fb6-eda3518af4b1', 'b11fe45b-0c2c-4551-9a01-d6206ebe9b00', 'IMAGE', 'https://cdn.chotot.com/IGxClNm2CCGkQdpHwMTdsAf-UP5T5F4zpBZR5Qj6Whg/preset:view/plain/4b66a1e302e177feada4079d3f652928-2996119647963304959.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('451c0d34-3c2d-4fd2-9a7b-c1888d060250', 'b11fe45b-0c2c-4551-9a01-d6206ebe9b00', 'IMAGE', 'https://cdn.chotot.com/J1kKi8D9ibOKI8CGCTjqF2ugdsJRUc2ZzyCI0mEIer0/preset:view/plain/aab2c60f7951afed745a3d5eb138949c-2996119648107842620.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('9468eaee-e64b-4605-86bd-4ea0b85abc01', 'P_133940220', 'APARTMENT', 'căn hộ Sinh Viên Giá Rẻ cửa sổ Thoáng Ngay Hậu Giang - Đại Học Mở', 'Dự án: 
Thông tin chi tiết: --Di Chuyển: Tân phú, Q11 ,Q10 ,Các quận trung tâm
🌐 Tiện ích toà nhà :
👉 Phù hợp với gia đinh, người đi làm, 
👉  NỘI THẤT: Như Ảnh 
👉 Cửa cổng vân tay, PCCC an toàn
👉 Khu vực an ninh, camera, có BẢO VỆ

✅ Liên hệ trực tiếp, ib Zalo ( Quốc Khánh) để được tư vấn và xem phòng nhanh nhất', 'AVAILABLE', 'Quận 6, Tp Hồ Chí Minh', 30, 3800000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8395dc2b-2b24-4db3-88a3-474e62ee3c03', '9468eaee-e64b-4605-86bd-4ea0b85abc01', 'IMAGE', 'https://cdn.chotot.com/zFtrbz6ZHtXxNaJrnMaRTEhzqvcwdFp4BfyuJE3PhyA/preset:view/plain/5cbaeb2e60b7c2eb8ff7ccde7a2a9c54-2996120110167148004.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('581634ed-adbd-4330-9442-1f45350f7eab', '9468eaee-e64b-4605-86bd-4ea0b85abc01', 'IMAGE', 'https://cdn.chotot.com/EuFQImfNPvfBwfufWspIk7RpAtkGf7fMMq3qqpDGrWU/preset:view/plain/8c55c1080a3124c4d683ba556680afff-2996120110169629732.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1076225f-a5b0-4570-9e0a-65b490ebfa44', '9468eaee-e64b-4605-86bd-4ea0b85abc01', 'IMAGE', 'https://cdn.chotot.com/iaXrp22xAhU2irc87ra9d8MeYolITpXRv5XAjWCYrvc/preset:view/plain/435ba090c06c711d7c3ceb0a95830ba9-2996120110283247207.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9086fa17-efc3-4701-a287-73124352f903', '9468eaee-e64b-4605-86bd-4ea0b85abc01', 'IMAGE', 'https://cdn.chotot.com/o0iHHpF2s0g5S6CcNBZlVN8voi187bhhjq9GiV7Vw58/preset:view/plain/0934722eac2f9505cde746ec2aa893fb-2996120110306114285.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('229e0630-c63f-4089-ac48-88654ea2cb33', '9468eaee-e64b-4605-86bd-4ea0b85abc01', 'IMAGE', 'https://cdn.chotot.com/9d9fMnF88sN3dzQQxlBRaFNeWy2ssKjNz1H4USTRDV4/preset:view/plain/6a19b45d601f6825d752faefc102642d-2996120110689785937.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7f181796-1e1c-4c6e-978e-bff6ce6a66a3', '9468eaee-e64b-4605-86bd-4ea0b85abc01', 'IMAGE', 'https://cdn.chotot.com/7BsuvDcjMZgZ8dVCoX05mOGbb666hIY7M-elHeC80Rw/preset:view/plain/05ba5ce7d94f380ded11240b7287be2e-2996120110614369279.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('81160031-226e-4423-9a89-6f7d5a75dc2b', '9468eaee-e64b-4605-86bd-4ea0b85abc01', 'IMAGE', 'https://cdn.chotot.com/grRjmAfPfkzfY85izA4CdRWb06sXPF-FsksECgFM8fU/preset:view/plain/f9da1791e879577688051afd7e1686b5-2996120110370618893.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('87ba755f-11dd-435e-87cc-6333d6045d89', 'P_131251287', 'APARTMENT', 'Cho thuê 2pn 2wc 62m2 trống 7tr, có nt 8tr; 3pn từ 8-10tr', 'Cho thuê căn hộ Dream Home Palace – Quận 8
Hiện bên mình có vài căn đang trống, khách có thể dọn vào ở ngay hoặc hẹn thời gian phù hợp:
🍀2PN 2WC (nhà trống): khoảng 7 triệu/tháng
2PN 2WC (có 3 máy lạnh + máy giặt): khoảng 7,5 triệu/tháng
2PN 2WC (nội thất gần đầy đủ): khoảng 8 triệu/tháng
🍀3PN 2WC (nhà trống): khoảng 8 triệu/tháng
3PN 2WC (có nội thất): tầm 9–10 triệu/tháng
Nhà sạch sẽ, thoáng, phù hợp ở gia đình hoặc nhóm bạn.
Anh/chị cần xem nhà hoặc hỏi thêm thông tin có thể liên hệ mình: ***', 'AVAILABLE', 'Quận 8, Tp Hồ Chí Minh', 62, 7000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f449190f-6b9f-42df-8815-da6d90b5936e', '87ba755f-11dd-435e-87cc-6333d6045d89', 'IMAGE', 'https://cdn.chotot.com/F5htnqwIdVAsf2ibUwZWK1fTEcEQo53uC6i-OpIfkq0/preset:view/plain/1a9dcea39fb8bc91bcdd40be56dd7dc2-2976535748837234386.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('94ea05e9-5b58-4e5c-87e9-8e1ddaa892ac', '87ba755f-11dd-435e-87cc-6333d6045d89', 'IMAGE', 'https://cdn.chotot.com/66Ku1aVLPTlwJLwxYu3zY4cWQEf0NUXbS9B7iBScFt4/preset:view/plain/f9cb4dc0d3be0e8fd7b7f2b52d1c8105-2976535748747773472.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('153c21ce-ee92-4709-bb23-8e411e6233be', '87ba755f-11dd-435e-87cc-6333d6045d89', 'IMAGE', 'https://cdn.chotot.com/9HNy73VW4UmmIwHsX0MqEZ723HPIqPbZT1Gb6c6GbiY/preset:view/plain/3978d4207fd4e6407fc70911876fc70c-2976535788348954322.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a5493e26-6178-4281-9241-ac58250fdf99', '87ba755f-11dd-435e-87cc-6333d6045d89', 'IMAGE', 'https://cdn.chotot.com/MAFt9YuvzR8zJVNz-N1mtFc5T3lsJVF5FtaEDykQHEc/preset:view/plain/b9de501ab2d2f633ed1532e85fa119d1-2976535788181116626.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a0d0736c-d389-42f9-97e0-dd080662da3c', '87ba755f-11dd-435e-87cc-6333d6045d89', 'IMAGE', 'https://cdn.chotot.com/VF5KalW0ZKPiV2cWR4PoU2MlgrdFtH0ExSkeeb0YGNI/preset:view/plain/7607037a11badd6e5c1aef8ee59f1e4f-2976535788345401052.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f35f2ef6-e7ae-4078-89dc-a636ab965f80', '87ba755f-11dd-435e-87cc-6333d6045d89', 'IMAGE', 'https://cdn.chotot.com/mUX6y40Ao9ELXOYHIFV8jn0tumpQCbEdwPeWeHPIC44/preset:view/plain/340ff1e8ddf50572a59c2fa3d37d0b76-2976535788326274592.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dca5d546-d491-4344-94a2-82a41b1989af', '87ba755f-11dd-435e-87cc-6333d6045d89', 'IMAGE', 'https://cdn.chotot.com/NZql0alMJ3cPAMYTXZ7peQ48WsoC_h_KFsGmkbQQ4L0/preset:view/plain/1b48ad2075e9ab8f0d18ecc415deb73c-2976535789051208975.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('084a12cc-c9f9-4a3a-9054-8522c4a03ac0', '87ba755f-11dd-435e-87cc-6333d6045d89', 'IMAGE', 'https://cdn.chotot.com/FedopY0a9xwC-h0MxngxVJsyiVyrGuIKIivx9Vj6DLg/preset:view/plain/0db27a4d90da17c34ab95405bc07a74d-2976535789120771794.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('7bad8907-4a18-4081-814b-8e4dc5176c36', 'P_133940198', 'APARTMENT', 'Dự Án mới 2PN 2WC Thang Máy, full nt, Phú Nhuận, 8tr9', 'Dự án: 
Thông tin chi tiết: Cho thuê căn hộ 2 phòng ngủ, 2 wc
Toạ lại: Ngay Nguyễn Kiệm, Phú Nhuận - Dưới chân cầu Hoàng Minh Giám, Thuận Tiện di chuyển Bình Thạnh, Gò Vấp, Sân Bay khu vực hotttt
Điện 4k
Nước 100/ng
Dv 200/phòng
Giá thuê 8tr9/th - Lộc cho người thiện chí
Thông tin thật
Liên hệ xem phòng: ***', 'AVAILABLE', 'Quận Phú Nhuận, Tp Hồ Chí Minh', 40, 8900000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('152ec065-76f5-48cc-ac14-206435d3bdf0', '7bad8907-4a18-4081-814b-8e4dc5176c36', 'IMAGE', 'https://cdn.chotot.com/zn9WnytyqSBAiVlQSBMFoLltNrA-Br36-CCZOOmOvtI/preset:view/plain/6d6ab46b99c919844df53db2484e413d-2996119958787878611.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c8501e73-2d50-405c-92e3-5ec979a21ef0', '7bad8907-4a18-4081-814b-8e4dc5176c36', 'IMAGE', 'https://cdn.chotot.com/9ISPUT_Ad4mWv5VIVdIvaxY8qZBsO4VzjlsBBMNKR7E/preset:view/plain/3acd4cfa55fca015778aeb4d977d0138-2996119959023074029.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7e5a82ce-bf3e-493f-b708-01f9e30b184c', '7bad8907-4a18-4081-814b-8e4dc5176c36', 'IMAGE', 'https://cdn.chotot.com/-qv-S2kPcPudvIDk4KPFcHbP6VeI_JhYsmQoMImmb_M/preset:view/plain/77884c730f9971ee4b616aaffc880d1c-2996119958956261336.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6ac1d027-b1b7-476d-bfbc-e5ade779c6f2', '7bad8907-4a18-4081-814b-8e4dc5176c36', 'IMAGE', 'https://cdn.chotot.com/7_r0OZ6uPSWT5hNVLpbJP6Kp4SQy41-D2CN8OyK7YX0/preset:view/plain/77e76e10ea2cb7d73675267eea0912ca-2996119959132064121.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('e8b9e18c-12ba-4966-8ea9-59b21dfde423', 'P_130483570', 'APARTMENT', 'CHO THUÊ CĂN HỘ MINI Q1 GẦN ĐH VĂN LANG - ĐH MỞ', '✅ CHO THUÊ CĂN HỘ MINI FULL NỘI THẤT DT: từ 18 - 36m vuông ❤️GIÁ CHỈ TỪ 5tr2  ❤️
✅ CÁCH ĐH VĂN LANG 100M - ĐH MỞ 50M
✅ KHU VỰC AN NINH. CÓ THANG MÁY LỚN, CỬA VÂN TAY
✅ GIỜ TỰ DO (KHÔNG CHUNG CHỦ). BẢO VỆ GIỮ XE 24 / 24
✅ MIỄN PHÍ MÁY GIẶT - WIFI CỰC MẠNH
✅ XUNG QUANH ĐẦY ĐỦ TIỆN ÍCH, SIÊU THỊ 24h (Vmart; Coopmart, chợ Cô Giang (50m)

✅LỐI ĐI RỘNG THOÁNG ĐẢM BẢO AN TOÀN PHÒNG CHÁY CHỮA CHÁY . 

✅CÁCH CHỢ BẾN THÀNH - PHỐ ĐI BỘ BÙI VIỆN 5 PHÚT (đi bộ)
---------------------------
📍ĐỊA CHỈ : 59 /10 HỒ HẢO HỚN PHƯỜNG CÔ GIANG QUẬN 1

Gọi sdt 09087**39 xem phòng trực tiếp từ 8:00-20:00 mỗi ngày (vui lòng gọi hẹn trước)

Miễn tiếp báo điện tử

(Có hợp tác mô giới)', 'SOLD', 'Quận 1, Tp Hồ Chí Minh', 24, 5200000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6605fc8f-6433-49ab-a1de-4e2c40d1c941', 'e8b9e18c-12ba-4966-8ea9-59b21dfde423', 'IMAGE', 'https://cdn.chotot.com/Vz7Qf1V9NtJTYAW1fEpImZBtDolx_JyMOUdyMAy8JLw/preset:view/plain/95f2e0ffafb527d290bba80ffc24e6de-2984802366615726740.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7319500d-d7e0-4f2b-87f8-98dca20e9701', 'e8b9e18c-12ba-4966-8ea9-59b21dfde423', 'IMAGE', 'https://cdn.chotot.com/YzfGbjiUEMOwamfmxB2hvF5V38uaM3RWJQtkuQYf23E/preset:view/plain/f5a133ff27b57dc8369e67ac22855c9d-2984802217984731796.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4f7195c5-e27e-49be-98ee-79e387847d72', 'e8b9e18c-12ba-4966-8ea9-59b21dfde423', 'IMAGE', 'https://cdn.chotot.com/0SkgkZjQcFr3xDg-HTlrx6ZrYo_EC7UVb3_13vkACBc/preset:view/plain/919405c02851c73fea9483182209b3d7-2984802251583655085.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3868c2b9-1a8c-41c6-b811-83d4a2a42b49', 'e8b9e18c-12ba-4966-8ea9-59b21dfde423', 'IMAGE', 'https://cdn.chotot.com/wnMcRN6J1HPY6fXO5eFoyVOej45R6eZyKM3B0lNybrA/preset:view/plain/ea2e31ce440ee1b72daf79941bd61bef-2984802278861567185.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ac717033-b36a-4881-8381-267664913775', 'e8b9e18c-12ba-4966-8ea9-59b21dfde423', 'IMAGE', 'https://cdn.chotot.com/T-0WRgQ_Tnr9DMoWyxfdZzjJYZ71mnowtipkGuZwchc/preset:view/plain/f0a36c3a32991a089fc516efc23865c8-2984802287989113199.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bbf55836-42b1-40b9-bb04-fbb41dc0eddc', 'e8b9e18c-12ba-4966-8ea9-59b21dfde423', 'IMAGE', 'https://cdn.chotot.com/v-2A9nMgvuJ8JC8XRtXw6j52UO4DUeQYmA4ali4Ih5c/preset:view/plain/ec3d4801afa7a3a5fbd1d73a3f6c8faf-2984802299548333265.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5589e04e-86ec-4410-ae66-ed132858bcac', 'e8b9e18c-12ba-4966-8ea9-59b21dfde423', 'IMAGE', 'https://cdn.chotot.com/K2Sc301uXfu9hudCdz-d0XJmZBm3ZDcMHv9EROnrknQ/preset:view/plain/24dc1728d638d13a288dc3408a5ea5fa-2984802307081630929.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('14bd6b41-04bd-46b2-bd00-fceeca7f9f17', 'P_122892796', 'APARTMENT', 'CHO THUÊ VINHOMES GRAND PARK QUẬN 9 GIÁ CHỈ TỪ 4.5TR TẶNG 6th WIFI', 'Chuyên cho thuê căn hộ Vinhomes Grand Park Quận 9. 
Tặng 300k-  500k khi khách hàng lắp wifi do Quý Khách hàng. 
Giá thuê tham chiếu Vinhomes Quận 9:
- Studio: Chỉ từ 4.5 triệu/tháng. 
- 1PN +: Chỉ từ 5 triệu/tháng.
- 2PN và 2PN +: Chỉ từ 5.5 triệu/tháng.
- 3PN: Chỉ từ 7.5 triệu/tháng.
Dự án vinhomes có đầy đủ tiện ích nội khu miễn phí: Như hồ bơi, công viên trung tâm , sân tập thể dục như bóng đá, tenis, bóng chuyền, cầu lông, bóng bàn... Ngoài ra Vinhomes Quận 9 mang đến cho cư dân 1 cuộc sống đầy đủ về tiện ích siêu thị, chợ, trường học..
Vinhomes Grand Park là đại đô thị nằm tại vị trí trung tâm Quận 9. Được quy hoạch hiện đại với rất nhiều tiện ích đẳng cấp để trở thành thành phố công viên và đại đô thị thông minh đẳng cấp quốc tế.
Sản phẩm đa dạng - giá cả hợp lý nhất và rẻ nhất - có đủ bàn giao từ chủ đầu tư - nội thất cơ bản - đầy đủ nội thất hoặc nội thất cao cấp.
Chúng tôi chuyên cho thuê Vinhomes Grand Park quận 9, hỗ trợ quý khách hàng thuê từ lúc chọn căn hộ đến làm hồ sơ thủ tục ở Vinhomes Quận 9.
Xem nhà lúc nào cũng được. 24/7.
Tư vấn hỗ trợ nhiệt tình, ân cần và trách nhiệm.
Chúng tôi tự tin giá cả hợp lý nhất thị trường.', 'AVAILABLE', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 47, 4500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9d302ae6-b309-4e25-be61-8ba6befc8fbd', '14bd6b41-04bd-46b2-bd00-fceeca7f9f17', 'IMAGE', 'https://cdn.chotot.com/gif7RFbVIHqxAiC_Ljec85H9eeHJgcaTyQBLebNQcWY/preset:view/plain/4123622396f6e25a89fa99da96d6f384-2977977441356947965.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('16a74a28-431c-464b-a311-f8d5055df490', '14bd6b41-04bd-46b2-bd00-fceeca7f9f17', 'IMAGE', 'https://cdn.chotot.com/Cd1_lFGewd2zLB33vIXzFeK7PyL_UBTUB7jdCEwmEng/preset:view/plain/bf2428a2981f6a0b50c0c78597894751-2977977441420346741.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('20ac5134-0b98-4238-b434-a8f8affd0573', '14bd6b41-04bd-46b2-bd00-fceeca7f9f17', 'IMAGE', 'https://cdn.chotot.com/OCScokVUcQnMUOiFGETGJRV2XOHfgdu3SEGhIGfzjts/preset:view/plain/5efd59aff50b85dc0bbaf56eb5ed3b6b-2977977441165433479.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3a1fd3b7-188c-427a-87fb-a506f9e38000', '14bd6b41-04bd-46b2-bd00-fceeca7f9f17', 'IMAGE', 'https://cdn.chotot.com/1ABOtnCfNND7SA18HG5t5Ra7WJ-fPlwr3vsQs3mMHQA/preset:view/plain/4fe08f8f84b948ed216855b4b13afd7e-2977977441238180955.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cf919429-e74c-4384-89d7-c42fde7d46f1', '14bd6b41-04bd-46b2-bd00-fceeca7f9f17', 'IMAGE', 'https://cdn.chotot.com/HogLUmSYV-gtsOaSrgp8C8G96PKLOHPtCINoi5e-Qyw/preset:view/plain/9b67d6066bb52e66c62b767c7d2b3705-2980006179719586783.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('447ef8fa-f728-444f-b090-10d0ffa0d513', '14bd6b41-04bd-46b2-bd00-fceeca7f9f17', 'IMAGE', 'https://cdn.chotot.com/1sT2mWaxzlqXhR7PxMF0fZ6G_blROZAMfKJt-tAJGDU/preset:view/plain/812e6d663643375e4fe14a419adf58dd-2980006178873719322.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0ce9a9d9-3544-4789-a18c-c14501534535', '14bd6b41-04bd-46b2-bd00-fceeca7f9f17', 'IMAGE', 'https://cdn.chotot.com/8IAPBkWk78wHizIATSiCfZQb9doTyXxTueDu08BpFc0/preset:view/plain/f570c7660777f27970a4308ad39bc855-2977977477311701501.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('14457731-e90f-4949-880a-11ef33e6ec09', '14bd6b41-04bd-46b2-bd00-fceeca7f9f17', 'IMAGE', 'https://cdn.chotot.com/l34ioSfPvVCDbfscn9fBCQUWadx4CtnYcDm2bqc2lVs/preset:view/plain/2589f2e591aafc020ca9ab3122e95fe6-2977977477299109077.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('782cf049-d5dc-4906-acd6-cd39b09141cd', '14bd6b41-04bd-46b2-bd00-fceeca7f9f17', 'IMAGE', 'https://cdn.chotot.com/Pz4KyZuM3_MictCeNqiXy5prDKjC8tevAkRmfOWKvqk/preset:view/plain/0cc44868fbbfdf8518c589c218792053-2980006178722281452.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('44bc6c40-c8fa-40f9-b432-946409362771', '14bd6b41-04bd-46b2-bd00-fceeca7f9f17', 'IMAGE', 'https://cdn.chotot.com/0U0HdAJiyJUHwlnsR3cWJW19me3SVzCYCyu7jpIUBio/preset:view/plain/462dab5fb1a1ba56e1782158bcb55514-2977977477131271381.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('cb96761e-9a87-4d74-a83b-e030f7becc54', '14bd6b41-04bd-46b2-bd00-fceeca7f9f17', 'IMAGE', 'https://cdn.chotot.com/48Pxt7lnPCFn2n8jLPA-k6omFcWPadkbHf1AuMkxpLM/preset:view/plain/229dc9ac50bd6491c0ed1890f297ed06-2980006180095006860.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('878a3ba5-f479-4a89-8f07-31efa0e64196', 'P_133857735', 'APARTMENT', 'NGAY CV LÀNG HOA - BAN CÔNG - FULL NỘI THẤT - MÁY GIẶT - MỚI 100%', '🏡 Thông tin căn hộ
✨ Diện tích 45m² rộng rãi, thoải mái
🍳 Máy giặt riêng tiện lợi
🌿 Ban công đón gió, nhiều ánh sáng tự nhiên
🪑 Full nội thất – Chỉ cần xách vali vào ở

📍 Vị trí cực tiện
✅ Hẻm ô tô 6m, taxi/Grab đón trả tận cửa
✅ Chỉ 5 phút đến Emart Phan Văn Trị, Lotte Mart Gò Vấp, ngân hàng, siêu thị và nhiều tiện ích khác
✅ 10–15 phút đến các trường: ĐH Công nghiệp TP.HCM (IUH), Văn Lang, Nguyễn Tất Thành, Trần Đại Nghĩa...
✅ Gần các trục đường lớn: Phạm Văn Chiêu, Quang Trung, Lê Văn Thọ, Thống Nhất, thuận tiện di chuyển khắp Gò Vấp và các quận lân cận.

💖 Ở đây bạn sẽ được
✔️ Nhà xe riêng có mái che
✔️ Máy giặt riêng trong phòng
✔️ Khóa cửa thông minh, an toàn, không lo quên chìa khóa
✔️ Camera an ninh 24/7
✔️ Hỗ trợ bảo trì nhanh khi cần
✔️ Vệ sinh khu vực chung hằng tuần
✔️ Giờ giấc tự do
✔️ Quản lý hỗ trợ nhiệt tình 24/7

✨ Phù hợp cho sinh viên, giảng viên và người đi làm đang học tập, làm việc tại Gò Vấp và khu vực lân cận.
💰 Chỉ 6.400.000đ/tháng

📍 Địa chỉ: 111/17/2A Phạm Văn Chiêu, P. An Hội Tây, TP.HCM
(Ngay ngã ba Nguyễn Văn Khối – Phạm Văn Chiêu)', 'AVAILABLE', 'Quận Gò Vấp, Tp Hồ Chí Minh', 45, 6400000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('24396b70-9953-44ca-8751-153ad314db7f', '878a3ba5-f479-4a89-8f07-31efa0e64196', 'IMAGE', 'https://cdn.chotot.com/wz5TRsAy0_HlgBOni1UHuVEqYiQ48jsrd5UasGVzstI/preset:view/plain/4217165237e32f9b335ae0edd751e52a-2995455321960827257.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bd02caad-4ff9-4e8e-a524-f34af01032c1', '878a3ba5-f479-4a89-8f07-31efa0e64196', 'IMAGE', 'https://cdn.chotot.com/8Uf5rBybDNmLzVsrXE8SGmXWw9ZenqnddA5A3zKCFY8/preset:view/plain/b5325431467103daebadef6210e19009-2995455354540714241.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b621b735-82e0-46ad-bcbd-4f85a49e68b4', '878a3ba5-f479-4a89-8f07-31efa0e64196', 'IMAGE', 'https://cdn.chotot.com/meBcV8kHRYeLso6uzDqxEFc-xqVLVuib2IKF56Rg7Cg/preset:view/plain/1d8fe7c01a6bdb8bf579da19b31b89f0-2995455364758104321.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a955e27c-9a5f-4eab-9336-f7da43f74387', '878a3ba5-f479-4a89-8f07-31efa0e64196', 'IMAGE', 'https://cdn.chotot.com/WIvpkssyhhJXYFrXzZJfFA6WXAToww9aojuGpdlMr-o/preset:view/plain/90a4cf988fa244bd225622879ede1dee-2995455374340147577.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bca30e5c-e148-4955-80bc-a87970a527ff', '878a3ba5-f479-4a89-8f07-31efa0e64196', 'IMAGE', 'https://cdn.chotot.com/A-a4zieg8FhX-kFnVtQxcqxkfGbHUEsEIEXdKOI8XeA/preset:view/plain/214fd5f91b6e193826bc0fe404a513a2-2995455384523258956.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('674a527e-ac7d-4eed-85f1-82ff6e6ccb53', '878a3ba5-f479-4a89-8f07-31efa0e64196', 'IMAGE', 'https://cdn.chotot.com/j9-WBfj7xu9Ldc5q3VWyD7YIknAC9mp6HzDPL1iwors/preset:view/plain/1412f9b752208bc467c2f1997f397efe-2995455393313319169.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3a1e27fd-37e1-43c3-92a2-8a6db9db0c6b', '878a3ba5-f479-4a89-8f07-31efa0e64196', 'IMAGE', 'https://cdn.chotot.com/-Bsc2mro3Picy_P0cO4dTaPd3rAqrzslVHxuktt1xT0/preset:view/plain/9624d6f206ceef9b40302513e7ade96f-2995455933646195065.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('5f552c5b-8901-479a-a5af-a826a07b840d', 'P_133064622', 'APARTMENT', 'CHO THUÊ CĂN HỘ STUDIO CỬA SỔ CỰC THOÁNG ĐẸP HIỆN ĐẠI', 'Dự án: 
Thông tin chi tiết: - Vị trí thuận lợi gần sân bay, giáp Phú Nhuận, xong xoay lăng Cha Cả, đường Trường Sơn, Thăng Long, Nguyễn Trọng Lội, Hậu Giang, Giải Phóng, Phan Thúc Duyên, sân banh Chảo Lửa,.....
- Toà nhà 4 lầu, ra vào vân tay, xe để trệt, camera 247, ko chung chủ
- Tòa ít phòng, an ninh, chủ nhà uy tín, nội thất hiện đại
Ngoài ra, với gần 4 năm làm việc trong lĩnh vực này, mình còn giỏ hàng nhiều căn, nhiều dạng khác nhau khu vực Tân Bình, Tân Phú và lân cận.', 'SOLD', 'Quận Tân Bình, Tp Hồ Chí Minh', 30, 6000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b5172dc7-b0c6-4c6b-82f3-d672b1c1b0f8', '5f552c5b-8901-479a-a5af-a826a07b840d', 'IMAGE', 'https://cdn.chotot.com/UZhBRULcJsPvsPUoqf78RTJ3S9JJEpYG34eN1FX_wuw/preset:view/plain/00f87151903cbd54806bf105cb3ce118-2989433345775558845.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('acf378e4-38e3-4466-8ee4-f530f232552a', '5f552c5b-8901-479a-a5af-a826a07b840d', 'IMAGE', 'https://cdn.chotot.com/ztcXgRKlhdZv6UCn86CK0iDFPae__A744ena8ngQRm4/preset:view/plain/1a3d76e489536af5dbbff58be1f04d82-2989433345991142001.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8cb4e656-7728-446d-9a5b-fd37978f6785', '5f552c5b-8901-479a-a5af-a826a07b840d', 'IMAGE', 'https://cdn.chotot.com/2bBeBPDElXQWxd_ZrL_1UaByH6ST6e26-93Y3FAj7XA/preset:view/plain/f894677482efc0112a435f5d1b99a632-2989433346215329743.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9b20a044-aaf1-48d5-b9cb-e169dbc88521', '5f552c5b-8901-479a-a5af-a826a07b840d', 'IMAGE', 'https://cdn.chotot.com/O9IO9c6GGKbYGBKioqyHcS_Z8UW8KeG0zpx-hCVD6ZQ/preset:view/plain/c69ed7ef8b9be6ed41ab9e214e5257a7-2989433346335334653.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d60b3ddf-4126-41c9-8e6e-429f656f8321', '5f552c5b-8901-479a-a5af-a826a07b840d', 'IMAGE', 'https://cdn.chotot.com/UCFxH7rOu16a4mNo1K2miy9d-40PYSPws4X3sb7yzec/preset:view/plain/6d130482eb8718be980464e9a54264a8-2989433346972934397.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('22c94172-c4fc-41f9-990e-0a5108d7cb25', '5f552c5b-8901-479a-a5af-a826a07b840d', 'IMAGE', 'https://cdn.chotot.com/Aq1jS-taYyKkbC8tUT6d20m7HG3E-aIPXhR0AYNNcHQ/preset:view/plain/f12264221baaf0a9b5132fdc031f4337-2989433346930731633.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('fe804fd6-696f-4ca7-9b16-6b43b076e7bf', '5f552c5b-8901-479a-a5af-a826a07b840d', 'IMAGE', 'https://cdn.chotot.com/a0rFzs_2noPmItDCl64imoOK6AqSQUwD3oLBCbgyjLY/preset:view/plain/d28feb6d5aa2fedc451aae9dd81674d9-2989433346866143421.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2da308b9-e6df-400e-8635-972ccc7c5e50', '5f552c5b-8901-479a-a5af-a826a07b840d', 'IMAGE', 'https://cdn.chotot.com/v2dd_dDO8WNB6MJl3MhLyWlfVBevU2EnWc5EcwZdIxw/preset:view/plain/32dc7b567123764b2e07955b4894154d-2989433346978584079.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2e07e840-8314-4b5a-99c2-49a547f96611', '5f552c5b-8901-479a-a5af-a826a07b840d', 'IMAGE', 'https://cdn.chotot.com/TDNq25TjnwuUrbVAXyxuJPQvDa9yKLZ5O84wSqwcsIo/preset:view/plain/b97269ec2391602797b13b9f0c47df88-2989433347020701647.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1f69c621-c614-44b9-87c5-84eba2614fd8', '5f552c5b-8901-479a-a5af-a826a07b840d', 'IMAGE', 'https://cdn.chotot.com/0KGrFV4enjG-hbPkOA7iroNMEbgDBRT4hSo5-2d87Sc/preset:view/plain/75cdd60f03bcf17c85eb56aa7fb0e478-2989433346951818916.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('77afe7d8-6ac7-4102-80d9-b4b4aed0e9ff', '5f552c5b-8901-479a-a5af-a826a07b840d', 'IMAGE', 'https://cdn.chotot.com/UjX0xNtPrBaRUGw00QRWE7iNmKsFXou8dGsseW3G0kk/preset:view/plain/3e5d3695b9ee6a0926b140b3643cc8f2-2989433347058208854.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('af8e9245-4f22-4873-a883-94ae4aea8878', 'P_133808409', 'APARTMENT', 'STUDIO BAN CÔNG FULL TIỆN NGHI NGAY PHAN HUY ÍCH🔥', 'Dự án: 
Thông tin chi tiết: Studio ban công mới kengg ngay gần Emart Phan Huy Ích  - Cầu tham lương

- Sẵn máy lạnh, giường, tủ áo, bếp, tủ lạnh +300/tháng 

- Ra vào tự do, có mây giặt chung 

LH Phụng xem phòng !', 'AVAILABLE', 'Quận Tân Bình, Tp Hồ Chí Minh', 25, 4500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('48bb9c5a-474c-40a4-86c7-5bff9c264b7f', 'af8e9245-4f22-4873-a883-94ae4aea8878', 'IMAGE', 'https://cdn.chotot.com/vx1cE50RntXNv0VcKz8OePBym2lybjcDjXoOytq34ZE/preset:view/plain/f76a87237b886c9f12ff46a081cdb8c6-2995114380728701458.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9e0799f7-75a1-4600-ad90-77d2399e5329', 'af8e9245-4f22-4873-a883-94ae4aea8878', 'IMAGE', 'https://cdn.chotot.com/bWJBMOpj8WSCHZQPsvp4seaHEest9-mXKMApf6MMuis/preset:view/plain/f065aa65b69b1b1c366e443f96e69e47-2995114380766139029.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dd4bab44-9932-43ee-b802-36a2d9fb5979', 'af8e9245-4f22-4873-a883-94ae4aea8878', 'IMAGE', 'https://cdn.chotot.com/uCRtd38suB7H2bUkPJh2Q0csirMJOXYndNOjkuTMnZU/preset:view/plain/5e1c2824af45465a3cacc1c98cbfbe4f-2995114380706057822.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9aee81ea-76b7-4d86-998c-9cbf95a4c711', 'af8e9245-4f22-4873-a883-94ae4aea8878', 'IMAGE', 'https://cdn.chotot.com/y8fnZ5Yd2ORjyhrsXOlbepf0rvIw4AFfedVOD_A7VKM/preset:view/plain/7a4914e5951f2a802c9ee470875631ec-2995114380611715080.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('40f1c2b3-aa37-4b11-8455-3bbc6e86e7d5', 'af8e9245-4f22-4873-a883-94ae4aea8878', 'IMAGE', 'https://cdn.chotot.com/g7C-uUvrYOCXa7lxUaVR5avT-goP1sJNgtUBQWrvpD4/preset:view/plain/d8ab3ad0c652ee1d4c7ac0973bbfaf28-2995114380791399268.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('16aa4c7c-bf3a-448d-a606-1a25d3287a07', 'af8e9245-4f22-4873-a883-94ae4aea8878', 'IMAGE', 'https://cdn.chotot.com/V5iY1pyHxpLY9o6OMIxL7B_8-D2NHBmlRKl2b4T-6Q8/preset:view/plain/f201de8770418abd117011f22de0a889-2995114380945249136.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8e5c88b7-3617-49f8-815b-159c8dc096cb', 'af8e9245-4f22-4873-a883-94ae4aea8878', 'IMAGE', 'https://cdn.chotot.com/_6CM2yWUPdlcw097AbvwYjfBoc0MIUybto6pZYfCXFE/preset:view/plain/0a845b7f014210792b5820d7429ea5d1-2995114380834059008.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('69549666-9731-493d-9494-a85076840cfc', 'af8e9245-4f22-4873-a883-94ae4aea8878', 'IMAGE', 'https://cdn.chotot.com/Ck9mIuia_EtzZnXyH5272nXoOCCDngpIDz2kjbFPcr8/preset:view/plain/0d5da3faa2bc2ce2ff5ece101b7f8c43-2995114381265667459.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('57ed57ca-d945-4926-abf7-6e5719977201', 'af8e9245-4f22-4873-a883-94ae4aea8878', 'IMAGE', 'https://cdn.chotot.com/4qtwIvZjw-5Qu_QsOK-oga8hZivf5Y3lQ4anKZBBOZA/preset:view/plain/5edfc0449b8ce842ffeff33a46c20a42-2995114381265695703.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('531ca95a-324c-49ea-9075-1212e55b36b1', 'P_130667715', 'APARTMENT', 'Bán gấp Căn hộ 74m2, MT Phạm Văn Đồng, View Landmark 81, Tặng nội thất', '- Đã có sổ hồng riêng, cư dân ở Full đủ
- Tặng nội thất điện tử
- Diện tích : 72m2, 2pn2wc, bancol, logia
- Tiện ích : hồ bơi, Gym, Spa, siêu thị Mini,...
- Liên hệ sớm xem nhà và sổ hồng', 'AVAILABLE', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 74, 3580000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('07138b25-0b7a-4cae-b507-df2cf1d4b711', '531ca95a-324c-49ea-9075-1212e55b36b1', 'IMAGE', 'https://cdn.chotot.com/t0Bxt7maN7QvRxOaDgzptJMHNJsiwMhIpcYZGiNM1Wc/preset:view/plain/7ac43c12eb87535873198246f8c9834b-2969995996684951151.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('51c7ef3a-bd80-4dbc-950c-3a82e2270051', '531ca95a-324c-49ea-9075-1212e55b36b1', 'IMAGE', 'https://cdn.chotot.com/u7kRTxKrX-aZwpm2bJy-vYMaGvuwDKEdI4cEF7Zc3T8/preset:view/plain/3ff16c9a1fcf6b7a2df52cd3b23f5e22-2969995996443382177.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('199ba67f-0a58-4693-acf6-6cf92882212e', '531ca95a-324c-49ea-9075-1212e55b36b1', 'IMAGE', 'https://cdn.chotot.com/dSeyz2z1vXwKYk6MctjFwOuwVLQ7asnU2du2AUQG7QU/preset:view/plain/695d4ef3de3c4d76d0dc7e7b73d7995b-2969995998586619317.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ebb87fc0-4620-4a7d-a274-891080b0f1f9', '531ca95a-324c-49ea-9075-1212e55b36b1', 'IMAGE', 'https://cdn.chotot.com/ZDwptDNCQ7mbI1oG3v0HFdaNqc02AHOrCi5m04TZS4w/preset:view/plain/6eb788df09b2ea8af58ba39c408d6c4e-2969995998672370286.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('6cd323b6-bfa9-413f-86df-6c64ae98f3b9', '531ca95a-324c-49ea-9075-1212e55b36b1', 'IMAGE', 'https://cdn.chotot.com/edlXF033bCQsNqN_xMPpQ0Htu04JKhor96xJ1kH9uZg/preset:view/plain/ef6a3c92052f8b96470991c97b66af9f-2969996000734316976.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('10635f9e-956b-4ef9-98a7-0b3e8d5581a5', 'P_133640233', 'APARTMENT', '🌹Duplex GÁC CAO - Rộng / Thang máy, bảo vệ gần Đầm Sen, Q11', 'Dự án: 
Thông tin chi tiết: CĂN HỘ DUPLEX MỚI NỘI THẤT CƠ BẢN - XINH XẮN 

🕋 Địa chỉ: Tô Hiệu - Hoà Bình, Luỹ Bán Bích, gần Đầm Sen, Q11, Q6, Q10. Sát các trường ĐH Văn Hiến, ĐH Hồng Bàng, ĐH Bách Khoa, ĐH Mở,.... 

•  Ra vào vân tay, Camera an ninh, Bảo vệ nhà xe 24/24
•  Nội thất đầy đủ, hỗ trợ set up nội thất theo yêu cầu
•  Nhà xe rộng rãi, khu vực chung sạch sẽ
• Xung quanh nhiều tiện ích

———————————————
▪️ 𝐇𝐨̂̃ 𝐭𝐫𝐨̛̣ 𝐭𝐢̀𝐦 𝐯𝐚̀ 𝐜𝐡𝐨 𝐭𝐡𝐮𝐞̂ 𝐜𝐚̆𝐧 𝐡𝐨̣̂ 𝐝𝐢̣𝐜𝐡 𝐯𝐮̣ 𝐓𝐏.𝐇𝐂𝐌
 Đa dạng loại phòng: 𝗦𝘁𝘂𝗱𝗶𝗼 – 𝗗𝘂𝗽𝗹𝗲𝘅 – 𝟭𝗣𝗡 – 𝟮𝗣𝗡

▪️ 𝐓𝐢̀𝐦 𝐏𝐡𝐨̀𝐧𝐠 𝐌𝐢𝐞̂̃𝐧 𝐏𝐡𝐢́ - 𝐋𝐢𝐞̂𝐧 𝐇𝐞̣̂:
☎️☎️Zalo/Call : Như', 'AVAILABLE', 'Quận Tân Phú, Tp Hồ Chí Minh', 30, 4200000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('835565db-b90a-440b-a2c9-ad69f9fb46fc', '10635f9e-956b-4ef9-98a7-0b3e8d5581a5', 'IMAGE', 'https://cdn.chotot.com/dG9-CNaUnci24Qktew_RlbW5Upk4amv5R6_FRc6G8nE/preset:view/plain/f6b7b9cb0aaddf8437b7f4c7ba8b3d96-2993822682212394920.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('928af553-be1d-49ae-b81e-3b5af687fe7e', '10635f9e-956b-4ef9-98a7-0b3e8d5581a5', 'IMAGE', 'https://cdn.chotot.com/Wv8eQsMVZpdsCa6JUtCfm-ODPiXCxlPwevCmPKZj0-Q/preset:view/plain/aad029b46b6d9229234cd4caa79b03bd-2993822682283939442.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('04611ba8-e6d4-401b-9c6c-c2d8e10fe605', '10635f9e-956b-4ef9-98a7-0b3e8d5581a5', 'IMAGE', 'https://cdn.chotot.com/Wpeo4eTHyRqwhi5g1u5EmMV-iF0bJW2rZg71rIvDCJ8/preset:view/plain/3ae56d33feb3f8c78e0f3b9469ca8af0-2993822682301826207.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bbf39b87-3723-4f33-8267-3b458a31c09c', '10635f9e-956b-4ef9-98a7-0b3e8d5581a5', 'IMAGE', 'https://cdn.chotot.com/VFQRIICRIxNA027xfaPbI-6UYFojAIIpUmAo0M3_kJs/preset:view/plain/5a06274f4041a41292e3ed059b56148f-2993822682322569567.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7ffd8562-7386-4a4d-8cbd-e855c1788911', '10635f9e-956b-4ef9-98a7-0b3e8d5581a5', 'IMAGE', 'https://cdn.chotot.com/Wz8rYdwr9eLiLfWr1KoXTlpcGSmdoWb8EOgBb7bGnpU/preset:view/plain/74ae28bf485965f3ffcc3ef7bc868c72-2993822682366494263.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('25fa9b56-0222-499d-a13d-c0447f869a38', '10635f9e-956b-4ef9-98a7-0b3e8d5581a5', 'IMAGE', 'https://cdn.chotot.com/h32c60p-nlo46Zq-IjqTQh-FJL0qsORFvF-En4q1Z50/preset:view/plain/45e0f6f688dcd863bb8641c64cc6ab17-2993822682380739298.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('dc9e09a3-197d-43c8-8eee-588e849be394', '10635f9e-956b-4ef9-98a7-0b3e8d5581a5', 'IMAGE', 'https://cdn.chotot.com/aQoCvvoK_CYzOk8e7udE_wOkaJcd_drs-4sQ3aAOJrc/preset:view/plain/194882c65344d7426dea273f27d59bc1-2993822682398519294.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c1208056-326e-42b1-8030-d861e575371d', '10635f9e-956b-4ef9-98a7-0b3e8d5581a5', 'IMAGE', 'https://cdn.chotot.com/WhMZto3DYkn51fUkllpjQHiML_Jr6W9bByq0oFy-2hk/preset:view/plain/ba09d7c6720ec524615f367665d135bc-2993822682465228198.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0f061668-e88d-403c-8922-dd3bff9d0994', '10635f9e-956b-4ef9-98a7-0b3e8d5581a5', 'IMAGE', 'https://cdn.chotot.com/31vqdnXBvPOV-3VqQbOK_0MHMDZdUVGBnxSDH5D_wLU/preset:view/plain/8631453de8c607afee0fc5f8a05ccb39-2993822682479805521.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a78d440c-6847-474d-93e2-1c84dbf5c442', '10635f9e-956b-4ef9-98a7-0b3e8d5581a5', 'IMAGE', 'https://cdn.chotot.com/xu8QeODqBx9kwPT2PCbXlHYpTMMxTEiSjpBbcospUQA/preset:view/plain/8860089ecfb7d1847b2fcf5d08d8fd11-2993822682444709696.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f4d04e94-ae81-440f-af58-bc2a47175d16', '10635f9e-956b-4ef9-98a7-0b3e8d5581a5', 'IMAGE', 'https://cdn.chotot.com/J5eIwBSNvfaF9-XXDi2Ugs1DOrFlHzfrlZTvG7f5Q28/preset:view/plain/36e286f53c5338c614206ea897102299-2993822682484536540.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3129d281-b0e9-409f-b601-8ffaa5d91f5b', '10635f9e-956b-4ef9-98a7-0b3e8d5581a5', 'IMAGE', 'https://cdn.chotot.com/5naLk5ADZdAqT_TJACcQusDamKwtnK5sa5iD0FRIhv8/preset:view/plain/64a958d8b51aca07fdcccca3fefef483-2993822682588668253.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('32720c7b-5f0e-4559-8050-4f38ccfb8f40', 'P_133940164', 'APARTMENT', 'GIẢM NGAY 500k-1000tr CHO KHÁCH Ở TRONG THÁNG 8  NÀY - HỔ TRỢ CHO SV', 'Dự án: 
Thông tin chi tiết: Nhà có bảo vệ - hầm xe rộng
Đặc biệt mặt tiền đường
Full nội thất 
Gần chợ và bách hoá xanh
Rộng 35m2 
Không chung chủ
Giờ giấc tự do
An ninh', 'SOLD', 'Quận Gò Vấp, Tp Hồ Chí Minh', 35, 4500000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('31f74c26-f3b8-4faa-87b5-d9c485c22fb0', '32720c7b-5f0e-4559-8050-4f38ccfb8f40', 'IMAGE', 'https://cdn.chotot.com/3M0OIlf4eG0Kl3beMSeUXLQDXT01mC06bVGvFidUAn4/preset:view/plain/15c3919af1509d7bbcb322657b8fcb38-2996119958384780324.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('508b27c0-1f76-47e0-90b4-d845bbee3c70', '32720c7b-5f0e-4559-8050-4f38ccfb8f40', 'IMAGE', 'https://cdn.chotot.com/VHpM2kyDoU4eJBmsP8NYiS1eEGBtrXqx9l1rmL1Jj8Q/preset:view/plain/8e37a3c7cdd7783be664ac53eb42d2a5-2996119958565275108.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d55456d4-c5b1-4f80-bd63-d64a69e0d77b', '32720c7b-5f0e-4559-8050-4f38ccfb8f40', 'IMAGE', 'https://cdn.chotot.com/rcL7cdg8CIZIfm1npS-B83mkhhuYAgKbuwUlbVHUbLY/preset:view/plain/13c00296a727cf7d99dc4bc9619d4a0d-2996119958464122471.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9cdd4682-b0bf-4841-ab05-bcfe8856e07a', '32720c7b-5f0e-4559-8050-4f38ccfb8f40', 'IMAGE', 'https://cdn.chotot.com/eYNBUiEtUbfeWt_X5SBjv2mAElyFEnqP5vhRjcTv9Fg/preset:view/plain/4377471bf66fd55fd71867d0a8d55d41-2996119958583976024.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f6754b6f-a741-4f9d-b819-9aa524bbe91c', '32720c7b-5f0e-4559-8050-4f38ccfb8f40', 'IMAGE', 'https://cdn.chotot.com/59Lwkcs-syHEDVp_pwqcQmK-Io4bxh5xPOInuwqhzsw/preset:view/plain/0872e3445ca50c0a2bdd5f81f80e9741-2996119958351919853.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2ed27843-c5fd-4667-8d8a-943b7c1af7de', '32720c7b-5f0e-4559-8050-4f38ccfb8f40', 'IMAGE', 'https://cdn.chotot.com/y-3942PBGyQKM-fUxIedmhCDdOZZ0IUz88U6sVaEpQA/preset:view/plain/3586bfc17c218875593ea79f11a23bff-2996119958504318831.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a8a56a83-9d55-45fc-8c4a-9f36207dc580', '32720c7b-5f0e-4559-8050-4f38ccfb8f40', 'IMAGE', 'https://cdn.chotot.com/v9G1tOl0YzHhswhf5GU5DxRSCjnUOKKUHwuSZgV07NQ/preset:view/plain/26beffefcebbd0d09972610d832bdc79-2996119958586955857.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('65c5bd7b-31f8-4845-8874-691e0a05abcd', '32720c7b-5f0e-4559-8050-4f38ccfb8f40', 'IMAGE', 'https://cdn.chotot.com/_4vEL2Oiy7P4WSRjUCdTwpSbNMZLpTPZP4HbsQAFLJs/preset:view/plain/0eb23ba8e63094422e0eb2cbb8894033-2996119958467351848.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d5b3b376-f835-4654-9d4b-168e5b33892d', '32720c7b-5f0e-4559-8050-4f38ccfb8f40', 'IMAGE', 'https://cdn.chotot.com/8s6m5y8Vl4QSeVwpM0Y1Q820VBqUxiz-9QfLJMCcqi0/preset:view/plain/e634ebbbc6919d75ad5fa0e0191bac9f-2996119958410578297.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('08ee693a-1613-42df-b9ce-14e02d5a4678', 'P_132804220', 'APARTMENT', 'CHO THUÊ CĂN HỘ 1 PHÒNG NGỦ FULL NỘI THẤT CAO CẤP - NGAY SÂN BAY', 'Dự án: 
Thông tin chi tiết: Căn Hộ 1 Phòng Ngủ 50M2 Full Nội Thất Cao Cấp - Ngay Sân Bay - 

Địa chỉ: Yên Thế, P2, Tân Bình
- nhà mới, thang máy, ra vào vân tay, an ninh
- diện tích 50m2 , full nội thất cao cấp như hình
- free xe, ở liền , mặt tiền đường oto', 'AVAILABLE', 'Quận Tân Bình, Tp Hồ Chí Minh', 50, 7000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5f765564-6c95-41a3-ad52-78c7a4a01849', '08ee693a-1613-42df-b9ce-14e02d5a4678', 'IMAGE', 'https://cdn.chotot.com/2f6vnsr9MNBcBZN7aUx8eTu6M7odw4Z9rTGfaawzIhE/preset:view/plain/1d64e9d7dd2bc2fd1b560a61f94adff0-2987430774809553615.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9625b82f-341b-4aef-bbd8-e9d14aaeac9c', '08ee693a-1613-42df-b9ce-14e02d5a4678', 'IMAGE', 'https://cdn.chotot.com/t9qHe4gzxO_CUk9X2c9i8fLfTf4sdZQYBxcnw6M_iyI/preset:view/plain/3b0e968fd1abb3b0356b9867e3e33fcf-2987430774991552078.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7c0c9427-4a9d-46f0-8f92-634de7c984f6', '08ee693a-1613-42df-b9ce-14e02d5a4678', 'IMAGE', 'https://cdn.chotot.com/eIwUgWrnIojOAtOP-IKF9F-WBmrDyrJFnBytrOb5Hks/preset:view/plain/1ca9f48f5b197ac84f77ed8c37a52fd0-2987430774911858157.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('02a1381a-9806-4dbf-8403-1c76b507ba7a', '08ee693a-1613-42df-b9ce-14e02d5a4678', 'IMAGE', 'https://cdn.chotot.com/NIRO5w_FkHqmCy4PWTa44EF2kiFpucRZPW_OtUSjOYA/preset:view/plain/d341c10f832ea2c6adf5f3bc15ef10c4-2987430774961225594.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e977e4fa-9780-4943-864f-29c027caa595', '08ee693a-1613-42df-b9ce-14e02d5a4678', 'IMAGE', 'https://cdn.chotot.com/7Cs-hj-Aryj-snziz7t6PXKpZqAgvJpxDimBzXFg1HM/preset:view/plain/e5d14e05b147e1c803579621357037ce-2987430774939062043.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('52a831ec-5a50-48ea-ad45-c5130e12a9ec', 'P_133940151', 'APARTMENT', 'Studio CS TRỜI mới xây, ngay SVĐ Phú Thọ - Vxoay Lê Đại Hành', 'Dự án: 
Thông tin chi tiết: CHDV STUDIO FULL NỘI THẤT - THANG MÁY - MỚI XÂY

📍Lạc Long Quân - Vòng xoay Lê Đại Hành 
Sát Nhà Thi Đấu Phú Thọ, gần ĐH Hồng Bàng, ĐH Văn Hiến, ĐH Bách Khoa 

- Thang máy di chuyển - Giờ giấc tự do - Không chung chủ 

- Giá phòng từ 5tr 

- Các phòng đều có cửa sổ thoáng / Ban công / 2PN 

- Anh chị ở gia đình 1-2 người hoặc sinh viên ở quá hợp lý 

Số lượng phòng có hạn. Anh chị quan tâm LH em Như hỗ trợ tư vấn & xem phòng', 'SOLD', 'Quận 11, Tp Hồ Chí Minh', 30, 5000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('0ad2830c-2bc5-4c68-b382-816108b43d32', '52a831ec-5a50-48ea-ad45-c5130e12a9ec', 'IMAGE', 'https://cdn.chotot.com/F_edndNYIUHqc2i49OXZWTXg03oWCpzhJt45SwmcFMI/preset:view/plain/af0845d882b878693ace7aaac6cfdf2d-2996119060366577255.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a8a96edc-8960-4de0-a986-4827864455f4', '52a831ec-5a50-48ea-ad45-c5130e12a9ec', 'IMAGE', 'https://cdn.chotot.com/3JWn6qTgkZc292CipQStnlBLAX_mIVmYlTemd764lwE/preset:view/plain/7df4611190f96def2b76686be817fbfb-2996119060380357928.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3a5e9990-f2ce-496a-9a09-5a83f5e55064', '52a831ec-5a50-48ea-ad45-c5130e12a9ec', 'IMAGE', 'https://cdn.chotot.com/pEZ1n5UB32zUHpwas-EgA-FZqakCqbD08NcJOWGcobc/preset:view/plain/4e2f46ed8b50164e0dd7c64d84ba71f8-2996119060858393599.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('5077204f-0223-4828-91d6-99656411c6ff', '52a831ec-5a50-48ea-ad45-c5130e12a9ec', 'IMAGE', 'https://cdn.chotot.com/Qlqz-LdclO9vcMzn6Tftqaz9iBr1dsVyD267Ho6MKr0/preset:view/plain/292ccfa1f5bbfaecfb0545b16ac1a848-2996119060500676109.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('8a14d737-e4c4-4d0f-ae4f-299945dd4fb8', '52a831ec-5a50-48ea-ad45-c5130e12a9ec', 'IMAGE', 'https://cdn.chotot.com/0iNj5uHKSWoe4VpQv9prf8pxYO-0jH7RzQCiMPQaX4I/preset:view/plain/28c78198876096f6c67fee980e2ca18e-2996119060441506852.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('805bb8fb-163d-452c-992c-4c04b7ad15d6', '52a831ec-5a50-48ea-ad45-c5130e12a9ec', 'IMAGE', 'https://cdn.chotot.com/3TkUII2Jbq428XIi24xcZqMVncnZ60EGKH4Vhw9L_Xg/preset:view/plain/a2357b817f40e64c8a34ff34e0c8def8-2996119060539259629.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('ae50517c-132f-4c03-91f8-66324d553de9', 'P_122102857', 'APARTMENT', 'Căn hộ Pn techcons, 3 phòng ngủ', 'Cho thuê căn hộ Pn techcons 48 Hoa Sứ,
 Phường 7,Quận Phú Nhuận, TP HCM. Diện tích :130m2, 3 phòng ngủ, 2 vệ sinh, phòng khách, bếp, ban công.. Giá thuê 24 triệu/tháng.Full nội thất cao cấp.Liên hệ xem nhà Ms Thúy', 'AVAILABLE', 'Quận Phú Nhuận, Tp Hồ Chí Minh', 130, 24000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3b9fec3a-adde-4f51-aa27-5ab1e3190888', 'ae50517c-132f-4c03-91f8-66324d553de9', 'IMAGE', 'https://cdn.chotot.com/xWdcRiikVTj7KPSMoZe5dZv8xEx1V_aWyLOVcBf2yAw/preset:view/plain/a26854a1fb75da6329c994f02eb98064-2912026093364933570.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d785b2e5-defa-46e0-a385-732bf117bc4e', 'ae50517c-132f-4c03-91f8-66324d553de9', 'IMAGE', 'https://cdn.chotot.com/foy0e-eidx2quTGCaFKV7mGRoZRDEyeKfFh3Up_AE-k/preset:view/plain/f45dc8513e38fbe163e317299ccb3152-2912026092558838656.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('64b474b5-91fd-4047-b0cd-f482d799a750', 'ae50517c-132f-4c03-91f8-66324d553de9', 'IMAGE', 'https://cdn.chotot.com/909JI8WWFwWZlrwKPQVc1eF0J9zydsUwPi5CM7YNHBQ/preset:view/plain/521d4246669483871b66ea0de050d50b-2988145142424289981.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d86e735e-509d-4758-a9c6-ba7d985805e3', 'ae50517c-132f-4c03-91f8-66324d553de9', 'IMAGE', 'https://cdn.chotot.com/cp6kblX_6eLUyNDHmP-DhVKdi2mst22hLTf10wS78Jg/preset:view/plain/46885bc00f813459e4a13b49072782d6-2988145169803215941.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('4d6e4f58-5ca8-4845-80ce-fabceaa3757a', 'P_133333453', 'APARTMENT', 'CHO THUÊ CHDV DUPLEX BAN CÔNG Q7 GẦN LOTTE MART, TDTU, UFM 5P QUA Q4', 'Dự án: 
Thông tin chi tiết: Cho thuê CHDV duplex trung tâm quận 7 có ban công - MÁY GIẶT RIÊNG
• Gần Lotte Mart, GO!, Phú Mỹ Hưng và Crescent Mall
• 5 phút qua Quận 4 bằng cầu Kênh Tẻ
• 10 phút di chuyển đến Quận 1
• Xung quanh đầy đủ quán ăn, cafe, cửa hàng tiện lợi, gym
• Toà nhà an ninh, khu vực yên tĩnh
• Ra vào vân tay/thẻ từ
Phù hợp người đi làm, cặp đôi hoặc khách thuê lâu dài cần không gian sống tiện nghi và thuận tiện di chuyển.
Zalo/WhatsApp: *** (Quân AP)
Hỗ trợ TƯ VẤN MIỄN PHÍ theo nhu cầu từng khách hàng đến khi tìm được phòng ưng ý nhất.
#canhoquan7dep #chothuecanhoq7 #studioquan7
#canholpnquan7 #fullntquan7 #canhogiarequan7 #canhomoiquan7 #canhodep #canhothangmay #canhobancong #phongtrodepquan/ #canhochinchu #canhoganquan7 #canhotiennghi #canhoganquan1
#canhoq7viewdep #canhodichvuquan7 #canhohimlamdep #canhogandaytienich #canhoquan7fullnt #chothuecanhodichvu #troquan7 #thuephongtro #chothuenhatroganTDTU #chothuecanhominiganUFM #chothuecanhominiganTDTU #chothuenhatroganUFM #chothuecanhodichvuganLotteMart #chothuecanhodichvuganCauTanThuan #chothuenhatroganLotteMart #chothuecanhomini #chothuenhatrophongtro', 'AVAILABLE', 'Quận 7, Tp Hồ Chí Minh', 40, 6000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f044d8a6-db0d-4ab7-ac6c-699bbdde3c83', '4d6e4f58-5ca8-4845-80ce-fabceaa3757a', 'IMAGE', 'https://cdn.chotot.com/DM74yaVTxQyOEnAM7aH1g2ot3L9eT6BZsmzFw4CydEA/preset:view/plain/4e447f2cfb8081c6e2ffd6172fee8c10-2996120788121296984.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e24eefdd-e057-417e-9aee-8be6b33d52a0', '4d6e4f58-5ca8-4845-80ce-fabceaa3757a', 'IMAGE', 'https://cdn.chotot.com/y3odMYeb7NZOkfBMLTNk68zltqygAZnn1vjUVwBGl3Q/preset:view/plain/76bcd9c424e7296d7f0e56115d4db073-2996120788421160914.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('defaf17c-ae17-41a1-a9da-6370f87702b4', '4d6e4f58-5ca8-4845-80ce-fabceaa3757a', 'IMAGE', 'https://cdn.chotot.com/8OXR-timpk41mfxr9-_2nCzSjucLBXEx4TEjgvRsqrA/preset:view/plain/f4214c624967af2f338e0cbd4bde1768-2996120788723125139.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c47ffc98-f56e-412d-8468-eba5f23e4360', '4d6e4f58-5ca8-4845-80ce-fabceaa3757a', 'IMAGE', 'https://cdn.chotot.com/Lc7fRm6Xe4fFRpPYpyMXsYjRmCOyqNc_tOefCmzXZKM/preset:view/plain/a5f68d802e64b1b7fe9027e16a212b1b-2996120788238695949.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2c1abaa4-e2f9-47e5-85c6-9987f284bb89', '4d6e4f58-5ca8-4845-80ce-fabceaa3757a', 'IMAGE', 'https://cdn.chotot.com/rik910ceeN-xh4swsgWr77QsgZ4drkX-CMcC5Y3fdKk/preset:view/plain/2fb861425f01ff35945e80749b4ee348-2996120787494556671.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e2f76954-e637-46fe-837c-a0d44d047654', '4d6e4f58-5ca8-4845-80ce-fabceaa3757a', 'IMAGE', 'https://cdn.chotot.com/Sx8CmjgwkCgqPt-B07lizs4Pkdm4DBx5ddREgLipUpY/preset:view/plain/1d7aa7eb311001f272acf921ee602253-2996120787551819857.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7cbd8b9e-a5f9-4b27-991c-73be9b517e40', '4d6e4f58-5ca8-4845-80ce-fabceaa3757a', 'IMAGE', 'https://cdn.chotot.com/4WTCdDgPwcqJi_uymFivDuPPCuCybheSGawB98F-37Y/preset:view/plain/95f5a4f2380dd43992d908b8dbdd43ea-2996120787499915417.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('c9b728b9-1cc8-4d28-ab06-500ca9ccb492', '4d6e4f58-5ca8-4845-80ce-fabceaa3757a', 'IMAGE', 'https://cdn.chotot.com/IMO532sAsAVY_Kgkta-op4bcVLJVFhKMucOAqd7hdy0/preset:view/plain/3936a7f34b3a97ba73f73cbc5f118025-2996120788035289129.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d1113bb9-8e85-44eb-a890-626cf59ac9e4', '4d6e4f58-5ca8-4845-80ce-fabceaa3757a', 'IMAGE', 'https://cdn.chotot.com/Esp8Mren6OEq6VgTh3FiRMyQQNbkGYqPTfDuJ5YhuYM/preset:view/plain/5b716b393a1efba5ecf7243ab6c26158-2996120788088088230.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('076b0bc7-0af4-434d-a533-2fb75d03a4de', '4d6e4f58-5ca8-4845-80ce-fabceaa3757a', 'IMAGE', 'https://cdn.chotot.com/3BKTGKdaAJXAqgcHK9QNhiePUXI4Uoe_Eu_7JdQWYdY/preset:view/plain/4eada41568eb1610b6189c0226090c9f-2996120788138872423.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('71f51237-8221-4567-a1bf-4b32b270793b', '4d6e4f58-5ca8-4845-80ce-fabceaa3757a', 'IMAGE', 'https://cdn.chotot.com/AyGDzZEMdKDUUeCzUBl4cfAIun1ttaf2Jm5MGg0rViA/preset:view/plain/fa1c195905706b3c6a80e56885c0f7d8-2996120788505015807.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3580d58f-ccb2-4c0c-a65b-a7bec99a12a6', '4d6e4f58-5ca8-4845-80ce-fabceaa3757a', 'IMAGE', 'https://cdn.chotot.com/r_7CZ-pcNgPrJ8MJaWnADI_2DO7ffaq8qLvJouRgYUU/preset:view/plain/890a9ab56a38fa8af6fb590079c5b2ed-2996120788488286241.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('b503b58f-6544-48cd-8944-57b3e7667d4a', 'P_130984032', 'APARTMENT', 'HƠN 15 CĂN PRECIA CHO THUÊ, GIÁ TỪ 13-15TR, CÓ NTCB HOẶC FULL', 'Giỏ hàng hơn 15 căn đang trống tại Precia, đa dạng diện tích và layout, phù hợp gia đình trẻ, chuyên gia làm việc khu Đông.

Giá thuê từ 13 – 15 triệu/tháng tùy căn, tùy nội thất.

Có sẵn:

Nhà nội thất cơ bản (NTCB)

Full nội thất, vào ở ngay

Hỗ trợ gửi hình thực tế từng căn, so sánh ưu – nhược điểm để khách chọn đúng nhu cầu và ngân sách.
Làm việc nhanh, hỗ trợ thương lượng giá cho khách thiện chí.

Anh/chị cần xem nhà hoặc nhận giỏ hàng chi tiết, liên hệ em gửi thông tin ngay.', 'AVAILABLE', 'Thành phố Thủ Đức, Tp Hồ Chí Minh', 68, 13000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('87a668c1-b805-4d9e-84d1-dddb9f9307cc', 'b503b58f-6544-48cd-8944-57b3e7667d4a', 'IMAGE', 'https://cdn.chotot.com/owgdHkUzK_0pQ0nt_xbnAowZDnNKj4H8tirFw9wx9HM/preset:view/plain/8c3371bd7e266049d17734e0b91b2477-2973910205030459005.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('2aca0960-1b9e-4886-98d5-59e5726ade79', 'b503b58f-6544-48cd-8944-57b3e7667d4a', 'IMAGE', 'https://cdn.chotot.com/tLBfoOLfOU0u-1U4JT-BbWT-Yd_n0Fy0TKNzziepmRM/preset:view/plain/39fad9800862e12c903181c137929eed-2973910205003127890.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e1418a62-0fae-4d06-aaa1-7d890d9a443d', 'b503b58f-6544-48cd-8944-57b3e7667d4a', 'IMAGE', 'https://cdn.chotot.com/GEGu2bmF_S5UoSWEHWQpug0kkjRhd8YuYSAqeM-Pbho/preset:view/plain/eabc483c3a446f8d2eb93effefaace6c-2973910204961140214.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('17a903f9-bba0-450b-9980-4001002e478d', 'b503b58f-6544-48cd-8944-57b3e7667d4a', 'IMAGE', 'https://cdn.chotot.com/LCFNbDWaaW2J_MUgpZyklXRdEx0yjh55aXTRITUX6Bk/preset:view/plain/9ebc63e571b0b418b100f1578a5bb7a6-2973910204966338938.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('460d9ef7-43ef-4d89-b17f-f67e6536ac68', 'b503b58f-6544-48cd-8944-57b3e7667d4a', 'IMAGE', 'https://cdn.chotot.com/Nf7L1jwD4WqjnCfJFF1WW7OjFb47w0YW3kiRl9QSKw0/preset:view/plain/9158e7725653ba3ec8e57700005478d6-2973910205175754234.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ee8e76a2-ceef-445f-9ec7-44af6225ce11', 'b503b58f-6544-48cd-8944-57b3e7667d4a', 'IMAGE', 'https://cdn.chotot.com/nAxYYGVzxZtiYguBMJzetbq_djZPtcbxoV3dP2QsbM0/preset:view/plain/6da3bd8f6ac99e527f3c8a13953e65a3-2973910205042688183.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('88e88d53-2e98-431c-ae7c-d81d9cd14f87', 'P_133827627', 'APARTMENT', 'Căn hộ Duplex full nội thất đường Điện Biên Phủ, Quận Bình Thạnh', 'Căn hộ Duplex full nội thất tại đường Điện Biên Phủ, Phường Thạnh Mỹ Tây, Quận Bình Thạnh.

Thông tin căn:
- Diện tích: 35 m²
- Thiết kế không gian Duplex, 1 WC
- Full nội thất
- Cửa sổ
- Thang máy

Vị trí thuận tiện:
- Gần ĐH Giao thông Vận tải TP.HCM
- Gần Ngã tư Hàng Xanh

Chi phí:
- Điện: 4.000đ/kWh
- Nước: 150.000đ/người
- Phí quản lý: 200.000đ/tháng

Liên hệ 3T Apartment để hẹn xem phòng.', 'AVAILABLE', 'Quận Bình Thạnh, Tp Hồ Chí Minh', 35, 6300000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('e4d7d5d0-0f27-4ed6-858a-f3518ec948e2', '88e88d53-2e98-431c-ae7c-d81d9cd14f87', 'IMAGE', 'https://cdn.chotot.com/V3Np9o7VlOvfSgjOEhKcjhu6N32ZzoXqseVjajvYI5o/preset:view/plain/7b1d395a65435e980ebdb2e487e72f9a-2995257776001182400.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('9b797086-db78-42c2-b3b8-7b30a19cb28b', '88e88d53-2e98-431c-ae7c-d81d9cd14f87', 'IMAGE', 'https://cdn.chotot.com/Am31KFh6jungavt39fijNwaYMyRFhvFijoa_sBekmhA/preset:view/plain/181aa5de2910b4846e18c1b1220f50bf-2995257776017763326.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ab0ff419-7db8-44fa-97e7-882efd1b1040', '88e88d53-2e98-431c-ae7c-d81d9cd14f87', 'IMAGE', 'https://cdn.chotot.com/-qCpNfbktdHG6Jgw0unipiIdhf8RYjwDjtB0Swsqn5s/preset:view/plain/36f6c8db6ffc5ab8810c69734f7b1c14-2995257776058002078.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('167a63b6-5713-43aa-a1a3-52676422d256', '88e88d53-2e98-431c-ae7c-d81d9cd14f87', 'IMAGE', 'https://cdn.chotot.com/gtzqjiZQUdKYUqGzHW5YQ_cOjW2sWpr2N7moOBHuUGM/preset:view/plain/39adad429cad39ad2c515b87d3398a53-2995257776051365036.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b8157e59-9ae1-414f-9605-41532f6caf21', '88e88d53-2e98-431c-ae7c-d81d9cd14f87', 'IMAGE', 'https://cdn.chotot.com/dOaFgSCbdmtYWIHgQTnP4fyVFQ6trFuzaL9Z7kzKli8/preset:view/plain/5e3f1f096fb8e2775eb7dfb4b9e50661-2995257776092412447.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('96446a03-de12-4f63-ad73-7aac6827bc3d', '88e88d53-2e98-431c-ae7c-d81d9cd14f87', 'IMAGE', 'https://cdn.chotot.com/jb7pn8lL_xw3feFXmT_wqyNltekWjoLb3urLQ9nT8jQ/preset:view/plain/9dd8c204b2cd6fb84d2e0fcaa71b14c5-2995257775960675184.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7009e481-f3a3-449b-9d9b-d5a9499d67cb', '88e88d53-2e98-431c-ae7c-d81d9cd14f87', 'IMAGE', 'https://cdn.chotot.com/yVMMH8G4HNI1Tcr47OMsN-RiFyD4xf2jBxEAFWvrYb0/preset:view/plain/7a8dcce5a256ccb3f13e32425aec8c02-2995257776097939944.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('a34be08c-8c4b-4156-87dd-057609ce9f30', '88e88d53-2e98-431c-ae7c-d81d9cd14f87', 'IMAGE', 'https://cdn.chotot.com/XZA1RSdqFzsa-H60juJ6QlETENudKJ87m3nFwNzTcms/preset:view/plain/29c3e4d521412ff42c18427ea9ea92f8-2995257776010291457.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('1fc316b1-5a99-41d9-8841-6b0abea8b7c0', 'P_133458879', 'APARTMENT', '🌟ĐỘC QUYỀN STUDIO BAN CÔNG - MÁY GIẶT RIÊNG - NGAY AEON TÂN PHÚ', 'Dự án: 
Thông tin chi tiết: CHO THUÊ CHDV STUDIO | - ĐẠI HỌC VĂN HIẾN #VHU - ĐẠI HỌC CÔNG THƯƠNG #HUIT

Địa chỉ: Tân Kì Tân Quý - Tân Quý - Tân Sơn Nhì - Aeon Tân Phú - Lê Trọng Tấn - Tây Thạnh - Gần ĐH Công Thương ,… - Quận 11 ,..) 

☑️ Khu vực an ninh, tiện ích xung quanh đầy đủ

☑️ Ra vào vân tay – Giờ giấc tự do

☑️ Camera 24/7 – PCCC an toàn

☑️ Full nội thất: máy lạnh, giường nệm, tủ áo, kệ tủ bếp, nước nóng NLMT, bàn ghế, máy giặt riêng,...

📞Xem phòng liên hệ em: ( Thành Truyền ) hỗ trợ ngay', 'AVAILABLE', 'Quận Tân Phú, Tp Hồ Chí Minh', 28, 5200000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('53358d79-05d5-43e7-b011-e3fffbe6a06e', '1fc316b1-5a99-41d9-8841-6b0abea8b7c0', 'IMAGE', 'https://cdn.chotot.com/mwkx8TfAA3Vt8Se1ydFb6ldAcb_qU50pjQyfvMW3TGA/preset:view/plain/08b036bb6ea92f81562adfda131326c9-2994080064964846873.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('ce51e8fc-85d7-4307-a42e-e6fd3f07e1f1', '1fc316b1-5a99-41d9-8841-6b0abea8b7c0', 'IMAGE', 'https://cdn.chotot.com/Sy-MVyxnuVZOmiveZJ2XeB0I8IVHP9iiJ5jrdDv9ea0/preset:view/plain/d0898b00972e36efec253c625b9ac09a-2994080065418048175.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f2180e56-8199-4df3-93f1-399934b0fe30', '1fc316b1-5a99-41d9-8841-6b0abea8b7c0', 'IMAGE', 'https://cdn.chotot.com/7VuDLoaGQbHVw_ndCtY7RBPJiI9d4688FwhhVZ6qj_Y/preset:view/plain/0a618f7c04477535cd7acaa01b757983-2994080065540964563.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('45d9c67c-a86c-4f0d-8dc4-25b70ed7820d', '1fc316b1-5a99-41d9-8841-6b0abea8b7c0', 'IMAGE', 'https://cdn.chotot.com/WFWESRkKfuB2spnFHar_kZf9_zOv5EifyUGN6TLLgM8/preset:view/plain/8b875f406b278014f36d17ceb8f119cf-2994080065597338404.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4eaf715c-b2e2-41ab-ae08-1e22cb9ca530', '1fc316b1-5a99-41d9-8841-6b0abea8b7c0', 'IMAGE', 'https://cdn.chotot.com/58j_Z8vZkoBEbJ2dDc3idjw9NBP5N5QYqwBtRwJ_ZPE/preset:view/plain/b69bc4d6edf16538055c80b6dd7c4400-2994080064973931679.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('587b703d-5d66-434e-b6a0-2d9e5f094f01', '1fc316b1-5a99-41d9-8841-6b0abea8b7c0', 'IMAGE', 'https://cdn.chotot.com/9qyYhwS_J_qEOOjaCV3CT2z9RyNItaHs0wDK4ge5BQo/preset:view/plain/e0d69d33217f0431a6fddda52586add2-2994080065285561692.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('d49d0832-38f0-4802-b146-aff3ac135514', '1fc316b1-5a99-41d9-8841-6b0abea8b7c0', 'IMAGE', 'https://cdn.chotot.com/5DOTOwwBjmZViQYa2LHSrk-qNjUCTEIbHXM2Yf3DabA/preset:view/plain/5651397a03073d45963a53637f4d08b5-2994080065354112543.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3f66fa0a-54cc-486a-9207-5abc5f74e86d', '1fc316b1-5a99-41d9-8841-6b0abea8b7c0', 'IMAGE', 'https://cdn.chotot.com/rib36rQ1uMSwn7pBMMttCmJHQiOvO1rLxlZS1RtiGD0/preset:view/plain/fbf7303c120631099086721502f7ec4f-2994080065457992894.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('56be0dd8-494e-4ff3-8622-065afcb9e63c', '1fc316b1-5a99-41d9-8841-6b0abea8b7c0', 'IMAGE', 'https://cdn.chotot.com/V_U4gsKZbhKvnwgZlXZYnDSE-U72tqdTHPzqkHpY-H4/preset:view/plain/e8995d27547389e0f673634229e52cf7-2994080065659083402.jpg', 8, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1061edbe-3ef1-4d10-9102-4c77b0c8c0b9', '1fc316b1-5a99-41d9-8841-6b0abea8b7c0', 'IMAGE', 'https://cdn.chotot.com/MVT3wtvzXXBn2DSM442Asi3oVx057HUPY-lJYhardfg/preset:view/plain/bd88973b51185ecfd0f17f3bddeff71e-2994080064796558073.jpg', 9, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('49c17e85-4302-4ee5-9e79-c892cbb66d67', '1fc316b1-5a99-41d9-8841-6b0abea8b7c0', 'IMAGE', 'https://cdn.chotot.com/658aObszAss2TPL8watsuftGB6X38qBPlt8X63xyn-k/preset:view/plain/7f7eb3b0d6a6ef31e8d67f2e57f67aa5-2994080065548123327.jpg', 10, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('12188318-3f6d-4063-825d-de6104fd5c6d', '1fc316b1-5a99-41d9-8841-6b0abea8b7c0', 'IMAGE', 'https://cdn.chotot.com/ZpIIg_YqBY7PWiifA8V7pII0nBZCHSP2-YuMEYepDv0/preset:view/plain/23ba958a41b4c0beb494ac3eaa293fec-2994080064758855984.jpg', 11, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('bb0040db-974f-4464-9c9b-1806cc0e2e70', 'P_133917797', 'APARTMENT', 'Chính Chủ Cho Thuê Phòng Ngay ĐH Hồng Bàng I Full Nội Thất Chỉ Từ 4tr', '📍 Địa chỉ: 64/17 Kênh Tân Hóa - Lò Gốm, Tân Thới Hòa, Tân Phú
📐 Diện tích: hơn 30m2

✨ Điểm nổi bật

✔ Nhà mới, sạch sẽ, thiết kế hiện đại
✔ Full nội thất – Chỉ cần xách vali vào ở
✔ Ban công, cửa sổ lớn, có bếp, cho nuôi thú cưng
✔ Không chung chủ – Ra vào linh hoạt
✔ Phù hợp người đi làm, sinh viên, cặp đôi...

🏢 Tiện ích:
🔐 Khóa cửa vân tay

📶 WiFi tốc độ cao

🛵 Bãi giữ xe

🐶 Cho phép nuôi thú cưng

🧺 Máy giặt

📍 Vị trí:

🚗 Gần Công viên nước Đầm Sen, đường 3/2, đường Hòa Bình, Kênh Tân Hóa, Khuông Việt, Lũy Bán Bích - nút giao các quận Bình Tân, Q11, Q10, Q5, Q6,...
🏫 Gần trường: ĐH Quốc Tế Hồng Bàng, Trung cấp Tây Nam Á, Trung cấp Phương Nam, Cao đẳng Quốc Tế, Hệ thống trường Quốc Tế Bamboo,..

🛍 Gần siêu thị: CoopMart Hòa Bình, 3 siêu thị Bách hóa xanh trong khu vực
🎁 Ưu đãi hiện tại
- Tặng ngay 1 ghế lười cho khách ký hợp đồng trong tháng, với hợp đồng từ 2 năm - giảm ngay trên giá thuê.

⭐ Vì sao nên thuê tại Happy Home?
✅ Hình ảnh & video thực tế
✅ Làm việc trực tiếp chính chủ
✅ Thông tin minh bạch
✅ Hỗ trợ xem phòng nhanh
✅ Tư vấn đúng nhu cầu, không phát sinh chi phí ngoài thông tin đã trao đổi

📲 Liên hệ ngay để nhận video thực tế hoặc đặt lịch xem phòng.

Happy Home – Giải pháp thuê phòng minh bạch.
Thuê dễ dàng – Sống an tâm.', 'AVAILABLE', 'Quận Tân Phú, Tp Hồ Chí Minh', 33, 4800000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('4cd38146-5266-4afb-8a25-e34f543f2c87', 'bb0040db-974f-4464-9c9b-1806cc0e2e70', 'IMAGE', 'https://cdn.chotot.com/JxHg1v9b2Vh7QBwN7nxlIe1vuPpkg3mwAxaeBOBNFwI/preset:view/plain/fefb25d6d2e164e409423eb4f29b08bc-2995957930701523441.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3a5b3926-af60-420e-b0dd-d7e8644d8eca', 'bb0040db-974f-4464-9c9b-1806cc0e2e70', 'IMAGE', 'https://cdn.chotot.com/jnV7cbRQ6gNaHkWKNl69zjFlS3qSxkMjBR_OnbVE71I/preset:view/plain/fda17deccf8711dc9ee3c38150d0bd93-2995957927026676835.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('34c8eab9-de1f-4565-9b92-576781c67d9c', 'bb0040db-974f-4464-9c9b-1806cc0e2e70', 'IMAGE', 'https://cdn.chotot.com/zgqDNi1FNnwi33i9VbKyrMKID9UHq_d4-CRD6RG2JuE/preset:view/plain/4c60d036b8847e593e456b6111551dc7-2995957925885760611.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('33a27fb7-4942-4e1c-90dd-7d8d56a0e474', 'bb0040db-974f-4464-9c9b-1806cc0e2e70', 'IMAGE', 'https://cdn.chotot.com/2g643gkhZGw8nvGggA0TIzXe8vtLMu07zCi6qp9bs0E/preset:view/plain/8ec4c9d8d131ae72ab31d7e76e54f0f2-2995957922305059425.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('97fb0839-8643-4d85-8b02-47d4ce2ebd41', 'bb0040db-974f-4464-9c9b-1806cc0e2e70', 'IMAGE', 'https://cdn.chotot.com/Ms-RtSOR8XFFN2lZ5e7C5BaFYAnObyYsYmpISS40998/preset:view/plain/744585c826980de0ebdbd16c11723cdc-2995957919987384917.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('18205165-ef65-4429-85f4-aad05c7ee763', 'bb0040db-974f-4464-9c9b-1806cc0e2e70', 'IMAGE', 'https://cdn.chotot.com/Wa9bXi13RLV1L-S6PZWWmLkx468DqYX8zC375Cfp_4E/preset:view/plain/36902a8e7bdb30dfc74cc40ef4c73b56-2995957929298936405.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('11c252fe-5e81-4b9c-92a9-dc7085261466', 'bb0040db-974f-4464-9c9b-1806cc0e2e70', 'IMAGE', 'https://cdn.chotot.com/jkSl_L2JOq6l-ORKVvXBOatBlx7T7GDtzXWXaP0ZEv0/preset:view/plain/24658fd71532a9ce474d0d1d522b8f13-2995957925811472761.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('af7a0676-39ac-48ee-86d5-518f84e2859c', 'P_131229034', 'APARTMENT', 'Charmington 1 phòng ngủ Full đẹp, view ko chắn thoáng xịn Quận 10', 'Charmington La Pointe - 181 Cao Thắng P12 Quận 10.

Full nội thất tốt đẹp , ban công view thoáng ko bị chắn

Giá thuê: 16 triệu/ tháng 
 - có cho thuê ngắn hạn từng tháng
- inbox e gởi video hình ảnh chi tiết nha 

Hồ bơi miễn phí, tiện ích đầy đủ.
Hầm xe rộng rãi, thẻ từ thang máy, an ninh tốt.

Rổ hàng e còn nhiều căn Studio giá từ 9tr5 - 14tr inbox e gởi thông tin chi tiết nhé.
--------
Hẹn xem nhà alo e nhé.
Quyên Quyên', 'SOLD', 'Quận 10, Tp Hồ Chí Minh', 50, 16000000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('65abbc39-83d5-4fb9-8872-2f86dd81f200', 'af7a0676-39ac-48ee-86d5-518f84e2859c', 'IMAGE', 'https://cdn.chotot.com/80YpKjpp4lsNFfJAAaIhOHpRCJmVsKpXb9-_0DYpJAk/preset:view/plain/e19ab743c71dda94144c3bd1173534f3-2981942327220479006.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('3e16c388-cecc-40d3-97ce-91c126c062a0', 'af7a0676-39ac-48ee-86d5-518f84e2859c', 'IMAGE', 'https://cdn.chotot.com/vxMpBtrVyVMNO8FraZsl_UK4FHui47jU629peWOodrw/preset:view/plain/6e482481d4b9faee5f32f3fb48680b8a-2975678977338808516.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('de95f160-c826-41b5-8285-b5c8a9b4e63b', 'af7a0676-39ac-48ee-86d5-518f84e2859c', 'IMAGE', 'https://cdn.chotot.com/dAFEmlrJHjEgQFuIkar24vrVb4KLDeUUAmbsY-gtCyM/preset:view/plain/2043146f389c69a7810d6040f4d5438e-2975678977030896267.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('f1d81f3c-9b7a-4aa5-9afc-5b2308ebd4b4', 'af7a0676-39ac-48ee-86d5-518f84e2859c', 'IMAGE', 'https://cdn.chotot.com/W2Z_-_GXFQxILgHC6IUkqt1cGT2ptsQJqXndubvowmk/preset:view/plain/6be9737c5f5117a833352b81b9ed68cb-2975678977659819646.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('b22be00f-a043-424f-ac62-2084e326d963', 'af7a0676-39ac-48ee-86d5-518f84e2859c', 'IMAGE', 'https://cdn.chotot.com/ygzRAxR8MWLNk9iQ5JXYodfgoduBgRCw06qQHc4_Tbo/preset:view/plain/d4ee7baa3edc881fe91fe43c813f02fd-2975678977539446259.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('1e2bc75d-7224-4b12-b930-080b08d00274', 'af7a0676-39ac-48ee-86d5-518f84e2859c', 'IMAGE', 'https://cdn.chotot.com/Ka7SZM-dpY4zUDA8H-SIh4dTU3Dm2wSsC7NekycyYJQ/preset:view/plain/1621c5de65872ff1b7030a87ccf50df5-2996123423656485924.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7aa46346-0335-450c-9d22-4347c29eba29', 'af7a0676-39ac-48ee-86d5-518f84e2859c', 'IMAGE', 'https://cdn.chotot.com/YZgOD0VD0EIUfqnRIhFmDODUBgBJmvCaNClrk1khuJk/preset:view/plain/4046ba69cbc1fc70e6af5441b1a1179f-2996123423623694713.jpg', 6, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7e04eead-5609-425f-b10f-b62ddcdf5265', 'af7a0676-39ac-48ee-86d5-518f84e2859c', 'IMAGE', 'https://cdn.chotot.com/NOXrf52tGgMDiDg1YBBT_nB34DhoMGnvJdLAdWQMdT8/preset:view/plain/7c9ab646675e1c036290f963edc9537f-2996123423679354152.jpg', 7, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO properties (id, code, property_kind, title, description, status, address_line, area_sqm, list_price, currency, province)
VALUES ('c236b8d4-8cfa-48d4-81b2-3ac7672e1744', 'P_133940114', 'APARTMENT', 'GIẢM NGAY 1tr CHO KHÁCH Ở TRONG THÁNG 8 - RỘNG 35m2 - FULL NỘI THẤT', 'Dự án: 
Thông tin chi tiết: Nhà mới 100% full nội thất có ban công
Có thang máy 
Hầm xe rộng
Giờ giấc tự do
Không chung chủ
Liên hệ em ạ', 'SOLD', 'Quận Gò Vấp, Tp Hồ Chí Minh', 35, 4150000, 'VND', 'Hồ Chí Minh') ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('248bab6f-9583-4be9-b382-dd9eec5e278f', 'c236b8d4-8cfa-48d4-81b2-3ac7672e1744', 'IMAGE', 'https://cdn.chotot.com/YcxVZS8yhjuzAoLwO0t8waAoSxDBVa8h825qQS2nxVk/preset:view/plain/76dd43a12b831ed02b81dd4416d161df-2996119741386429736.jpg', 0, TRUE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('564528fd-237d-4b97-b5e2-76c1b7f6c903', 'c236b8d4-8cfa-48d4-81b2-3ac7672e1744', 'IMAGE', 'https://cdn.chotot.com/08AdCXSjwhVbcmWYUySLYHkWcHLuB9dR2CFJXcCfLvs/preset:view/plain/f30371146e9675e7e9ce7c6b1773efcd-2996119741084050468.jpg', 1, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('18b60305-f495-4e18-840e-7193860cf33a', 'c236b8d4-8cfa-48d4-81b2-3ac7672e1744', 'IMAGE', 'https://cdn.chotot.com/DJ_sBlpZCZQVZP0K7SsdIPnmViMjECgO_Nhugs15WHE/preset:view/plain/e4475e6bb97d0bd8e981a1ff606d991b-2996119741169440921.jpg', 2, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('bc7cc60e-02f3-4ff5-8760-6d7e8066dc9b', 'c236b8d4-8cfa-48d4-81b2-3ac7672e1744', 'IMAGE', 'https://cdn.chotot.com/pegMRnbGqB4F2yOSfIHcD93hqcrtp3LOwWUUqUj4aHU/preset:view/plain/e54cc0fb4b099d9ee3c672fa8e97a7fa-2996119741421688913.jpg', 3, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('7e045746-a4ff-4deb-9e74-176af8a4cd1a', 'c236b8d4-8cfa-48d4-81b2-3ac7672e1744', 'IMAGE', 'https://cdn.chotot.com/5oXiMmgZs-RLM5otyG4tAuwqI1NynmTC3Zh5chIW0fI/preset:view/plain/f17b6a38e29fc480b10f6a52f312d3b4-2996119741217185880.jpg', 4, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
VALUES ('efb6a959-8166-4ae6-bf0d-b7e358578d3e', 'c236b8d4-8cfa-48d4-81b2-3ac7672e1744', 'IMAGE', 'https://cdn.chotot.com/_hUtmtyjZHTqEIsnjot8jJYzj6dyhgQzVescE6WRafo/preset:view/plain/d4a0a54fcc1cf9f16a0d37fbef7e9e1c-2996119741405232653.jpg', 5, FALSE) ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('b52b1740-b61c-4dae-915c-9039dc677710', 'REQ-10', '345ae931-45ac-47b9-b71f-de9d5066e333', 'd9c22b0e-0b7b-4592-97aa-841aab32000f', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('11098277-6d92-4807-915f-f09f5a4a60f7', 'b52b1740-b61c-4dae-915c-9039dc677710', '6e71b008-9825-4628-9790-375875048ca1', 'SELECTED', '2026-08-08 14:00:00+07', '2026-08-08 14:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('ac113c58-e807-44a7-a28e-6b1d7469eb69', 'b52b1740-b61c-4dae-915c-9039dc677710', '11098277-6d92-4807-915f-f09f5a4a60f7', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('1505e3cb-7725-451c-8a56-13694ad543dc', 'BKG-10', 'b52b1740-b61c-4dae-915c-9039dc677710', 'ac113c58-e807-44a7-a28e-6b1d7469eb69', '345ae931-45ac-47b9-b71f-de9d5066e333', 'd9c22b0e-0b7b-4592-97aa-841aab32000f', '6e71b008-9825-4628-9790-375875048ca1', 'CONFIRMED', '2026-08-08 14:00:00+07', '2026-08-08 14:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('e7cdbfb9-bfc4-4472-8c32-cc28a20918dd', 'REQ-12', '8d56a5be-25d6-4d65-a7bf-8b8d09809c3c', '024257ad-144c-40ce-98df-285e7e5372a6', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('38d29353-0944-4092-9207-330b062e5f8b', 'e7cdbfb9-bfc4-4472-8c32-cc28a20918dd', '595adcab-6060-4a0a-81c1-eb238a20dabf', 'SELECTED', '2026-08-10 10:30:00+07', '2026-08-10 10:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('56c3cb9d-40a8-4c0a-8995-358529c29142', 'e7cdbfb9-bfc4-4472-8c32-cc28a20918dd', '38d29353-0944-4092-9207-330b062e5f8b', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('c547cbe6-0dd6-4f66-b058-ff7dd69be244', 'BKG-12', 'e7cdbfb9-bfc4-4472-8c32-cc28a20918dd', '56c3cb9d-40a8-4c0a-8995-358529c29142', '8d56a5be-25d6-4d65-a7bf-8b8d09809c3c', '024257ad-144c-40ce-98df-285e7e5372a6', '595adcab-6060-4a0a-81c1-eb238a20dabf', 'CONFIRMED', '2026-08-10 10:30:00+07', '2026-08-10 10:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('017d9efc-137e-497c-b385-54f281d72463', 'REQ-20', '0c6b41b9-d6a8-4268-b954-3bab904a9e1f', '1fad41d8-c8eb-4462-b213-7a219a46847c', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('0fe807fc-5df1-4a1b-a26a-a1a29a5ee1c7', '017d9efc-137e-497c-b385-54f281d72463', '595adcab-6060-4a0a-81c1-eb238a20dabf', 'SELECTED', '2026-08-10 15:30:00+07', '2026-08-10 15:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('0455020a-4a28-49b0-9ca1-d1b31921d8e2', '017d9efc-137e-497c-b385-54f281d72463', '0fe807fc-5df1-4a1b-a26a-a1a29a5ee1c7', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('55cbe1b7-6e88-4863-873a-99bd0a36794e', 'BKG-20', '017d9efc-137e-497c-b385-54f281d72463', '0455020a-4a28-49b0-9ca1-d1b31921d8e2', '0c6b41b9-d6a8-4268-b954-3bab904a9e1f', '1fad41d8-c8eb-4462-b213-7a219a46847c', '595adcab-6060-4a0a-81c1-eb238a20dabf', 'CONFIRMED', '2026-08-10 15:30:00+07', '2026-08-10 15:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('b8ec201e-8def-46e5-bcd5-8d276b476158', 'REQ-27', 'cdae9859-b5a6-4e95-9f26-8042e60ad1c5', '6ba642f2-4bd1-401c-876e-229056c0cee6', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('90869bb6-562f-4383-a5ed-cc1f7be1a73c', 'b8ec201e-8def-46e5-bcd5-8d276b476158', '45988484-9573-493b-98f4-6e9e7e631e6e', 'SELECTED', '2026-08-12 17:00:00+07', '2026-08-12 17:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('2fe3e937-3ee0-41ee-8a34-0e835bfe7052', 'b8ec201e-8def-46e5-bcd5-8d276b476158', '90869bb6-562f-4383-a5ed-cc1f7be1a73c', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('ce83b122-f931-4c47-b520-76dd27e605a0', 'BKG-27', 'b8ec201e-8def-46e5-bcd5-8d276b476158', '2fe3e937-3ee0-41ee-8a34-0e835bfe7052', 'cdae9859-b5a6-4e95-9f26-8042e60ad1c5', '6ba642f2-4bd1-401c-876e-229056c0cee6', '45988484-9573-493b-98f4-6e9e7e631e6e', 'CONFIRMED', '2026-08-12 17:00:00+07', '2026-08-12 17:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('5ef2a5bd-8260-4e54-a4ed-6d4d417c3a23', 'REQ-28', 'c7aa753f-0e33-4c92-ac86-4a904815c30e', '55f57485-6faf-4059-84c4-cb18afffcff3', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('9b493f72-bcce-48b6-b244-6cf10345c17e', '5ef2a5bd-8260-4e54-a4ed-6d4d417c3a23', '19759e56-f845-4ce3-b05b-04971fc2d91d', 'SELECTED', '2026-08-10 09:00:00+07', '2026-08-10 09:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('2d1b3520-7a6f-4656-bfd4-3eafbcfc1911', '5ef2a5bd-8260-4e54-a4ed-6d4d417c3a23', '9b493f72-bcce-48b6-b244-6cf10345c17e', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('b5b2ad72-ac30-41f1-8d9e-045710298fd8', 'BKG-28', '5ef2a5bd-8260-4e54-a4ed-6d4d417c3a23', '2d1b3520-7a6f-4656-bfd4-3eafbcfc1911', 'c7aa753f-0e33-4c92-ac86-4a904815c30e', '55f57485-6faf-4059-84c4-cb18afffcff3', '19759e56-f845-4ce3-b05b-04971fc2d91d', 'CONFIRMED', '2026-08-10 09:00:00+07', '2026-08-10 09:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('6251817b-f5b4-4e3e-ab42-a90418347cfd', 'REQ-31', '445bd67e-ead3-4553-a9e9-0a156a68e61e', 'c236b8d4-8cfa-48d4-81b2-3ac7672e1744', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('c502d94e-cc81-4886-8185-7597fcc0317a', '6251817b-f5b4-4e3e-ab42-a90418347cfd', '595adcab-6060-4a0a-81c1-eb238a20dabf', 'SELECTED', '2026-08-06 17:00:00+07', '2026-08-06 17:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('ccfa3052-6423-48f3-956e-73bbcd890fbd', '6251817b-f5b4-4e3e-ab42-a90418347cfd', 'c502d94e-cc81-4886-8185-7597fcc0317a', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('4ab0d9a7-d85d-4599-ac82-769b7698489f', 'BKG-31', '6251817b-f5b4-4e3e-ab42-a90418347cfd', 'ccfa3052-6423-48f3-956e-73bbcd890fbd', '445bd67e-ead3-4553-a9e9-0a156a68e61e', 'c236b8d4-8cfa-48d4-81b2-3ac7672e1744', '595adcab-6060-4a0a-81c1-eb238a20dabf', 'CONFIRMED', '2026-08-06 17:00:00+07', '2026-08-06 17:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('77c9f861-2073-4221-a015-8c12606dcebe', 'REQ-37', '951118ab-8658-4ec2-86b8-09aa4afd07e6', 'f5a0c47c-3967-4e28-8528-4f2f30f8f2b9', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('33432b15-bc00-4950-9dba-e9ddceb489ea', '77c9f861-2073-4221-a015-8c12606dcebe', '19759e56-f845-4ce3-b05b-04971fc2d91d', 'SELECTED', '2026-08-04 10:30:00+07', '2026-08-04 10:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('12ccc81a-fd25-432a-94d0-1116d8b602a1', '77c9f861-2073-4221-a015-8c12606dcebe', '33432b15-bc00-4950-9dba-e9ddceb489ea', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('b3edf605-16e8-49d7-9cfe-52a9870eab24', 'BKG-37', '77c9f861-2073-4221-a015-8c12606dcebe', '12ccc81a-fd25-432a-94d0-1116d8b602a1', '951118ab-8658-4ec2-86b8-09aa4afd07e6', 'f5a0c47c-3967-4e28-8528-4f2f30f8f2b9', '19759e56-f845-4ce3-b05b-04971fc2d91d', 'CONFIRMED', '2026-08-04 10:30:00+07', '2026-08-04 10:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('9f48bce3-a47d-405e-abf9-bb81e310d057', 'REQ-38', '345ae931-45ac-47b9-b71f-de9d5066e333', 'ddec13ed-e0ac-434a-b423-b9eeba3e50c4', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('1b1602a4-5e5d-4e66-b578-e5009bcae45e', '9f48bce3-a47d-405e-abf9-bb81e310d057', '25db544d-b636-482c-95ce-102c3c6864d1', 'SELECTED', '2026-08-12 09:00:00+07', '2026-08-12 09:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('7c9a6a16-b208-4e0e-9781-a5058c8160d6', '9f48bce3-a47d-405e-abf9-bb81e310d057', '1b1602a4-5e5d-4e66-b578-e5009bcae45e', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('718d0d30-d5a9-4f95-b4ea-224a847819c3', 'BKG-38', '9f48bce3-a47d-405e-abf9-bb81e310d057', '7c9a6a16-b208-4e0e-9781-a5058c8160d6', '345ae931-45ac-47b9-b71f-de9d5066e333', 'ddec13ed-e0ac-434a-b423-b9eeba3e50c4', '25db544d-b636-482c-95ce-102c3c6864d1', 'CONFIRMED', '2026-08-12 09:00:00+07', '2026-08-12 09:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('543bab8e-28bb-40f9-8418-abf5b40926ca', 'REQ-39', '013e01ac-8a38-4082-863e-b59e860c4d7d', 'a8119d3f-d1bc-4706-8bbb-986ee182147f', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('7be2d459-dc89-40d6-aa6f-bbf7e64bf617', '543bab8e-28bb-40f9-8418-abf5b40926ca', '93cf20fd-efc6-4b60-b286-8324f310474c', 'SELECTED', '2026-08-07 17:00:00+07', '2026-08-07 17:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('f5d7de40-88d2-44d5-9a58-716da5d4df49', '543bab8e-28bb-40f9-8418-abf5b40926ca', '7be2d459-dc89-40d6-aa6f-bbf7e64bf617', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('6522216b-2fc8-4fce-a2ff-5bbdd21f465d', 'BKG-39', '543bab8e-28bb-40f9-8418-abf5b40926ca', 'f5d7de40-88d2-44d5-9a58-716da5d4df49', '013e01ac-8a38-4082-863e-b59e860c4d7d', 'a8119d3f-d1bc-4706-8bbb-986ee182147f', '93cf20fd-efc6-4b60-b286-8324f310474c', 'CONFIRMED', '2026-08-07 17:00:00+07', '2026-08-07 17:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('40b50d5f-64fb-4612-a52f-635338c7d950', 'REQ-41', '4fb71bc9-7dac-4a6a-8f33-7b61015c46af', '024257ad-144c-40ce-98df-285e7e5372a6', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('12ccb1ab-e015-4d37-a401-14a4ff47df69', '40b50d5f-64fb-4612-a52f-635338c7d950', '93cf20fd-efc6-4b60-b286-8324f310474c', 'SELECTED', '2026-08-09 09:00:00+07', '2026-08-09 09:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('16bf1081-e3cb-40f5-8754-29f9766c15e0', '40b50d5f-64fb-4612-a52f-635338c7d950', '12ccb1ab-e015-4d37-a401-14a4ff47df69', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('2b5e9582-2811-45bf-8378-072a18b69832', 'BKG-41', '40b50d5f-64fb-4612-a52f-635338c7d950', '16bf1081-e3cb-40f5-8754-29f9766c15e0', '4fb71bc9-7dac-4a6a-8f33-7b61015c46af', '024257ad-144c-40ce-98df-285e7e5372a6', '93cf20fd-efc6-4b60-b286-8324f310474c', 'CONFIRMED', '2026-08-09 09:00:00+07', '2026-08-09 09:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('9849db85-14bb-4eac-919c-26fc588894f1', 'REQ-44', 'f3ee0d29-4795-4815-a5ec-96aeaf24e4b6', '819828ab-44b6-4d48-9864-de4700a73d55', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('3a003de9-4496-4477-9524-53fec8267f8d', '9849db85-14bb-4eac-919c-26fc588894f1', 'ff169240-13ee-4788-8624-768d78db78fc', 'SELECTED', '2026-08-07 09:00:00+07', '2026-08-07 09:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('39f3b449-5fc7-4405-9b2d-175990b8694d', '9849db85-14bb-4eac-919c-26fc588894f1', '3a003de9-4496-4477-9524-53fec8267f8d', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('e9878ce8-1d16-4a27-baee-8c52bae146fc', 'BKG-44', '9849db85-14bb-4eac-919c-26fc588894f1', '39f3b449-5fc7-4405-9b2d-175990b8694d', 'f3ee0d29-4795-4815-a5ec-96aeaf24e4b6', '819828ab-44b6-4d48-9864-de4700a73d55', 'ff169240-13ee-4788-8624-768d78db78fc', 'CONFIRMED', '2026-08-07 09:00:00+07', '2026-08-07 09:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('974ff729-c994-4ff9-a4e5-ef5985b68f45', 'REQ-45', '3878efb3-ac1d-4607-9841-f1a05590022f', '0a107bee-d1f8-4943-8f7b-df734575a32f', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('42c50034-fcf0-4da1-99fd-e3772b219cb1', '974ff729-c994-4ff9-a4e5-ef5985b68f45', '1923b3f3-5600-4e41-a297-2ab6948698f5', 'SELECTED', '2026-08-12 14:00:00+07', '2026-08-12 14:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('56cd9e3a-4616-460d-8049-620887e46e01', '974ff729-c994-4ff9-a4e5-ef5985b68f45', '42c50034-fcf0-4da1-99fd-e3772b219cb1', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('2cd462f0-eb4d-4240-8199-6a3d2e73ad08', 'BKG-45', '974ff729-c994-4ff9-a4e5-ef5985b68f45', '56cd9e3a-4616-460d-8049-620887e46e01', '3878efb3-ac1d-4607-9841-f1a05590022f', '0a107bee-d1f8-4943-8f7b-df734575a32f', '1923b3f3-5600-4e41-a297-2ab6948698f5', 'CONFIRMED', '2026-08-12 14:00:00+07', '2026-08-12 14:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('8d3cd67c-36dc-4b56-8176-9b0c2ef32668', 'REQ-49', '8d56a5be-25d6-4d65-a7bf-8b8d09809c3c', '13e6be09-2829-4636-8222-6419672bd7ab', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('692e739a-e162-4930-bf02-22560f051569', '8d3cd67c-36dc-4b56-8176-9b0c2ef32668', '6c3d3653-e6bb-4301-b612-2517c2744784', 'SELECTED', '2026-08-13 15:30:00+07', '2026-08-13 15:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('7626ed45-ebff-4518-9ded-e2a27fe17263', '8d3cd67c-36dc-4b56-8176-9b0c2ef32668', '692e739a-e162-4930-bf02-22560f051569', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('5ccdf015-2b7f-42b3-a86c-9a468e52a2d6', 'BKG-49', '8d3cd67c-36dc-4b56-8176-9b0c2ef32668', '7626ed45-ebff-4518-9ded-e2a27fe17263', '8d56a5be-25d6-4d65-a7bf-8b8d09809c3c', '13e6be09-2829-4636-8222-6419672bd7ab', '6c3d3653-e6bb-4301-b612-2517c2744784', 'CONFIRMED', '2026-08-13 15:30:00+07', '2026-08-13 15:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('8e79b51e-ce09-4290-8961-0f30c53d360c', 'REQ-53', '5803c767-587c-4d81-9554-f9bdc672762d', '1eae53d4-fb4c-4429-bfb4-07b79fa505a5', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('f706dc05-847b-4465-bbd3-cb1cd3051d99', '8e79b51e-ce09-4290-8961-0f30c53d360c', '595adcab-6060-4a0a-81c1-eb238a20dabf', 'SELECTED', '2026-08-11 14:00:00+07', '2026-08-11 14:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('3c9ac0c9-9382-4b85-a8a2-d171a7014fe7', '8e79b51e-ce09-4290-8961-0f30c53d360c', 'f706dc05-847b-4465-bbd3-cb1cd3051d99', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('f166a710-489e-4f1c-a60f-ca529eaf9112', 'BKG-53', '8e79b51e-ce09-4290-8961-0f30c53d360c', '3c9ac0c9-9382-4b85-a8a2-d171a7014fe7', '5803c767-587c-4d81-9554-f9bdc672762d', '1eae53d4-fb4c-4429-bfb4-07b79fa505a5', '595adcab-6060-4a0a-81c1-eb238a20dabf', 'CONFIRMED', '2026-08-11 14:00:00+07', '2026-08-11 14:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('e93701a9-2d00-410b-acb3-5dde3c156d0b', 'REQ-59', '84e68e2b-0b42-4cdd-9023-823e0fab9fbe', 'c236b8d4-8cfa-48d4-81b2-3ac7672e1744', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('6e9e464c-5574-4fe3-a8e2-8fc6963defd6', 'e93701a9-2d00-410b-acb3-5dde3c156d0b', '93cf20fd-efc6-4b60-b286-8324f310474c', 'SELECTED', '2026-08-11 09:00:00+07', '2026-08-11 09:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('d222e9b2-7617-40bb-91e3-b1657f763326', 'e93701a9-2d00-410b-acb3-5dde3c156d0b', '6e9e464c-5574-4fe3-a8e2-8fc6963defd6', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('73c5b1a8-58aa-4afb-9e34-60abf35a92be', 'BKG-59', 'e93701a9-2d00-410b-acb3-5dde3c156d0b', 'd222e9b2-7617-40bb-91e3-b1657f763326', '84e68e2b-0b42-4cdd-9023-823e0fab9fbe', 'c236b8d4-8cfa-48d4-81b2-3ac7672e1744', '93cf20fd-efc6-4b60-b286-8324f310474c', 'CONFIRMED', '2026-08-11 09:00:00+07', '2026-08-11 09:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('2435960f-61b5-4f1e-8e90-9f62c2f884ae', 'REQ-61', '0c6b41b9-d6a8-4268-b954-3bab904a9e1f', '08ee693a-1613-42df-b9ce-14e02d5a4678', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('d88f7a37-14e7-4475-9598-f0a064002075', '2435960f-61b5-4f1e-8e90-9f62c2f884ae', '6c3d3653-e6bb-4301-b612-2517c2744784', 'SELECTED', '2026-08-11 14:00:00+07', '2026-08-11 14:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('7a6b94a7-1d80-415e-aa7d-16ec2dc3bc0d', '2435960f-61b5-4f1e-8e90-9f62c2f884ae', 'd88f7a37-14e7-4475-9598-f0a064002075', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('b98556f1-6d0a-4588-87f7-1e235f80988d', 'BKG-61', '2435960f-61b5-4f1e-8e90-9f62c2f884ae', '7a6b94a7-1d80-415e-aa7d-16ec2dc3bc0d', '0c6b41b9-d6a8-4268-b954-3bab904a9e1f', '08ee693a-1613-42df-b9ce-14e02d5a4678', '6c3d3653-e6bb-4301-b612-2517c2744784', 'CONFIRMED', '2026-08-11 14:00:00+07', '2026-08-11 14:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('220880d9-d0f2-478c-b981-57b1731f23a5', 'REQ-62', '013e01ac-8a38-4082-863e-b59e860c4d7d', 'db93d6b5-7c1b-47a8-8e0f-2f1749bd9f04', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('7b1fcf76-8e29-4454-aead-166637e45972', '220880d9-d0f2-478c-b981-57b1731f23a5', 'e7249ca8-47a8-4952-8f33-1a5bb456d7e4', 'SELECTED', '2026-08-04 17:00:00+07', '2026-08-04 17:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('f81ab093-c4ec-4bb6-8886-e18584256d33', '220880d9-d0f2-478c-b981-57b1731f23a5', '7b1fcf76-8e29-4454-aead-166637e45972', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('adf17a59-bfe4-4a7e-8713-691bf2d0e4fc', 'BKG-62', '220880d9-d0f2-478c-b981-57b1731f23a5', 'f81ab093-c4ec-4bb6-8886-e18584256d33', '013e01ac-8a38-4082-863e-b59e860c4d7d', 'db93d6b5-7c1b-47a8-8e0f-2f1749bd9f04', 'e7249ca8-47a8-4952-8f33-1a5bb456d7e4', 'CONFIRMED', '2026-08-04 17:00:00+07', '2026-08-04 17:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('8a4cc8b0-6983-4346-93b7-294652638b91', 'REQ-64', '753113b2-3020-41ae-9e7d-f8448c2978e1', 'c31398b1-bf7a-449b-9da2-268144e9c82d', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('6d87cb89-9d52-43e0-a1c4-276f99b3b55f', '8a4cc8b0-6983-4346-93b7-294652638b91', 'a83c97ee-e832-4e44-93aa-ef4031eb6358', 'SELECTED', '2026-08-12 15:30:00+07', '2026-08-12 15:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('5508aca5-c4c9-4392-9ab6-b26ec5a9aa6a', '8a4cc8b0-6983-4346-93b7-294652638b91', '6d87cb89-9d52-43e0-a1c4-276f99b3b55f', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('6ae502cf-ee6e-4ede-88f0-11bf06232dc2', 'BKG-64', '8a4cc8b0-6983-4346-93b7-294652638b91', '5508aca5-c4c9-4392-9ab6-b26ec5a9aa6a', '753113b2-3020-41ae-9e7d-f8448c2978e1', 'c31398b1-bf7a-449b-9da2-268144e9c82d', 'a83c97ee-e832-4e44-93aa-ef4031eb6358', 'CONFIRMED', '2026-08-12 15:30:00+07', '2026-08-12 15:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('bea880c0-8e1c-43bd-9470-0b6faefc83bc', 'REQ-65', '59a7951d-57fc-46b7-9358-e73976a4d9fb', '7f9a802c-f638-4073-a906-e60e1cd3ced8', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('1dece5ad-3bdb-41cb-b7eb-a0636d20aa36', 'bea880c0-8e1c-43bd-9470-0b6faefc83bc', '956c3b8b-2e9e-4e40-aa11-c88a74e4f2ac', 'SELECTED', '2026-08-13 17:00:00+07', '2026-08-13 17:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('639871ea-4158-40b7-aaf9-148923b7cac0', 'bea880c0-8e1c-43bd-9470-0b6faefc83bc', '1dece5ad-3bdb-41cb-b7eb-a0636d20aa36', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('3e61a7bb-7e95-4161-bc27-0c001a72ed2e', 'BKG-65', 'bea880c0-8e1c-43bd-9470-0b6faefc83bc', '639871ea-4158-40b7-aaf9-148923b7cac0', '59a7951d-57fc-46b7-9358-e73976a4d9fb', '7f9a802c-f638-4073-a906-e60e1cd3ced8', '956c3b8b-2e9e-4e40-aa11-c88a74e4f2ac', 'CONFIRMED', '2026-08-13 17:00:00+07', '2026-08-13 17:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('86eb98f0-cf45-4943-83cc-5df09f27de93', 'REQ-68', '7f996c13-fef5-4116-9c64-3847af14fceb', '13abd4c1-2b48-4b0a-9ba6-803a614027e9', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('62fc80df-6dd5-4cd8-af42-5c451a8358c9', '86eb98f0-cf45-4943-83cc-5df09f27de93', '83c30720-7756-4038-9086-e6c69336cfe8', 'SELECTED', '2026-08-07 17:00:00+07', '2026-08-07 17:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('c652a6f1-f884-426e-86ec-5ae9c8eb0955', '86eb98f0-cf45-4943-83cc-5df09f27de93', '62fc80df-6dd5-4cd8-af42-5c451a8358c9', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('9c42d906-f5e0-40c3-b96f-08e2d4931bdd', 'BKG-68', '86eb98f0-cf45-4943-83cc-5df09f27de93', 'c652a6f1-f884-426e-86ec-5ae9c8eb0955', '7f996c13-fef5-4116-9c64-3847af14fceb', '13abd4c1-2b48-4b0a-9ba6-803a614027e9', '83c30720-7756-4038-9086-e6c69336cfe8', 'CONFIRMED', '2026-08-07 17:00:00+07', '2026-08-07 17:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('3b90e95c-116a-412f-9fd2-7b174f0e0b56', 'REQ-70', '1e1ffb55-177f-47bb-9b55-1ee1f75c9813', 'e9e74b76-b636-4b2b-9640-a49fa124f074', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('bd8bd178-d0bd-4c43-ad2a-a250eeb9cf52', '3b90e95c-116a-412f-9fd2-7b174f0e0b56', 'd4442132-86b7-40cc-8522-37f248b64f0b', 'SELECTED', '2026-08-08 17:00:00+07', '2026-08-08 17:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('5db4685e-6b62-40b9-a422-f7207e2e0ab2', '3b90e95c-116a-412f-9fd2-7b174f0e0b56', 'bd8bd178-d0bd-4c43-ad2a-a250eeb9cf52', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('ae7f0da6-a125-439b-b05f-dcce459a8385', 'BKG-70', '3b90e95c-116a-412f-9fd2-7b174f0e0b56', '5db4685e-6b62-40b9-a422-f7207e2e0ab2', '1e1ffb55-177f-47bb-9b55-1ee1f75c9813', 'e9e74b76-b636-4b2b-9640-a49fa124f074', 'd4442132-86b7-40cc-8522-37f248b64f0b', 'CONFIRMED', '2026-08-08 17:00:00+07', '2026-08-08 17:59:59+07') ON CONFLICT DO NOTHING;
INSERT INTO tour_requests (id, request_code, customer_user_id, property_id, status)
VALUES ('92ce979b-f4df-4a94-8d17-cdf4cb7999b6', 'REQ-71', 'ca445c6d-04c3-4ce2-9491-762faf919202', '8bb46c6c-08e4-40ab-a742-2e5b313256f2', 'BOOKED') ON CONFLICT DO NOTHING;
INSERT INTO tour_slot_options (id, tour_request_id, sale_user_id, status, starts_at, ends_at, valid_until)
VALUES ('6ab53669-f128-4827-9ea9-9af06af6e752', '92ce979b-f4df-4a94-8d17-cdf4cb7999b6', '19759e56-f845-4ce3-b05b-04971fc2d91d', 'SELECTED', '2026-08-04 09:00:00+07', '2026-08-04 09:59:59+07', '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO approval_requests (id, tour_request_id, slot_option_id, status, requested_at, expires_at)
VALUES ('2046ea06-16d3-45b4-a015-f670bb886114', '92ce979b-f4df-4a94-8d17-cdf4cb7999b6', '6ab53669-f128-4827-9ea9-9af06af6e752', 'APPROVED', now(), '2030-01-01') ON CONFLICT DO NOTHING;
INSERT INTO appointments (id, booking_code, tour_request_id, approval_request_id, customer_user_id, property_id, sale_user_id, status, starts_at, ends_at)
VALUES ('9ca676d8-9a7c-4db5-9813-8e083ce5b8fd', 'BKG-71', '92ce979b-f4df-4a94-8d17-cdf4cb7999b6', '2046ea06-16d3-45b4-a015-f670bb886114', 'ca445c6d-04c3-4ce2-9491-762faf919202', '8bb46c6c-08e4-40ab-a742-2e5b313256f2', '19759e56-f845-4ce3-b05b-04971fc2d91d', 'CONFIRMED', '2026-08-04 09:00:00+07', '2026-08-04 09:59:59+07') ON CONFLICT DO NOTHING;
COMMIT;
