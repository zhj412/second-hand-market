/*
 Navicat Premium Data Transfer

 Source Server         : 本地数据库mysql
 Source Server Type    : MySQL
 Source Server Version : 100428
 Source Host           : localhost:3306
 Source Schema         : second_hand_market

 Target Server Type    : MySQL
 Target Server Version : 100428
 File Encoding         : 65001

 Date: 02/07/2026 09:00:56
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 53 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add 用户信息', 7, 'add_userprofile');
INSERT INTO `auth_permission` VALUES (26, 'Can change 用户信息', 7, 'change_userprofile');
INSERT INTO `auth_permission` VALUES (27, 'Can delete 用户信息', 7, 'delete_userprofile');
INSERT INTO `auth_permission` VALUES (28, 'Can view 用户信息', 7, 'view_userprofile');
INSERT INTO `auth_permission` VALUES (29, 'Can add 商品分类', 8, 'add_category');
INSERT INTO `auth_permission` VALUES (30, 'Can change 商品分类', 8, 'change_category');
INSERT INTO `auth_permission` VALUES (31, 'Can delete 商品分类', 8, 'delete_category');
INSERT INTO `auth_permission` VALUES (32, 'Can view 商品分类', 8, 'view_category');
INSERT INTO `auth_permission` VALUES (33, 'Can add 商品信息', 9, 'add_goods');
INSERT INTO `auth_permission` VALUES (34, 'Can change 商品信息', 9, 'change_goods');
INSERT INTO `auth_permission` VALUES (35, 'Can delete 商品信息', 9, 'delete_goods');
INSERT INTO `auth_permission` VALUES (36, 'Can view 商品信息', 9, 'view_goods');
INSERT INTO `auth_permission` VALUES (37, 'Can add 购物车', 10, 'add_cart');
INSERT INTO `auth_permission` VALUES (38, 'Can change 购物车', 10, 'change_cart');
INSERT INTO `auth_permission` VALUES (39, 'Can delete 购物车', 10, 'delete_cart');
INSERT INTO `auth_permission` VALUES (40, 'Can view 购物车', 10, 'view_cart');
INSERT INTO `auth_permission` VALUES (41, 'Can add 订单', 11, 'add_order');
INSERT INTO `auth_permission` VALUES (42, 'Can change 订单', 11, 'change_order');
INSERT INTO `auth_permission` VALUES (43, 'Can delete 订单', 11, 'delete_order');
INSERT INTO `auth_permission` VALUES (44, 'Can view 订单', 11, 'view_order');
INSERT INTO `auth_permission` VALUES (45, 'Can add 收藏', 12, 'add_favorite');
INSERT INTO `auth_permission` VALUES (46, 'Can change 收藏', 12, 'change_favorite');
INSERT INTO `auth_permission` VALUES (47, 'Can delete 收藏', 12, 'delete_favorite');
INSERT INTO `auth_permission` VALUES (48, 'Can view 收藏', 12, 'view_favorite');
INSERT INTO `auth_permission` VALUES (49, 'Can add 消息', 13, 'add_message');
INSERT INTO `auth_permission` VALUES (50, 'Can change 消息', 13, 'change_message');
INSERT INTO `auth_permission` VALUES (51, 'Can delete 消息', 13, 'delete_message');
INSERT INTO `auth_permission` VALUES (52, 'Can view 消息', 13, 'view_message');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$600000$fUGmiPBk7qTAuFUk1VaDtr$lCW8qdGuT4L0EH+JJfs3NBuyVjFfw4mf0idjlBZ89pE=', '2026-07-02 00:59:56.921899', 1, 'admin', '', '', 'admin@example.com', 1, 1, '2026-06-27 17:40:46.420804');
INSERT INTO `auth_user` VALUES (2, 'pbkdf2_sha256$600000$k9LQZtljbT8D5otG8iS0Au$GhbVhTQXBvVzRKS7+lr/1jbliELaxEqGQJCrFHgIuy8=', NULL, 0, 'user1', '', '', 'user1@example.com', 0, 1, '2026-06-27 17:42:24.300510');
INSERT INTO `auth_user` VALUES (3, 'pbkdf2_sha256$600000$wsxwzcJHHNtzrRnCZBExfr$TalH0cKMGPjf6plEXjBzUwc5krUn3bBqcNwysshRDTY=', NULL, 0, 'user2', '', '', 'user2@example.com', 0, 1, '2026-06-27 17:42:24.533586');
INSERT INTO `auth_user` VALUES (4, 'pbkdf2_sha256$600000$ITGQ7ic2mAYspJWijf3sYo$K8Q/prdSj1obLGrRSwxLG+4MgSUFOox0i74FHRzLKD0=', NULL, 0, 'user3', '', '', 'user3@example.com', 0, 1, '2026-06-27 17:42:24.730557');
INSERT INTO `auth_user` VALUES (5, 'pbkdf2_sha256$600000$BoZ9MkbE9iAIR1CWfJTYMn$oNE4CHqLL367jD8+IAo53nYs2jLPwDlbForkPBJd5s0=', NULL, 0, 'user4', '', '', 'user4@example.com', 0, 1, '2026-06-27 17:42:24.920570');
INSERT INTO `auth_user` VALUES (6, 'pbkdf2_sha256$600000$8BRZLEPNsd76X6JjZf0PYl$0uJygOOhD9yTDdHNLfntas+RhbBjl7wnRNZJQyXzfwo=', NULL, 0, 'user5', '', '', 'user5@example.com', 0, 1, '2026-06-27 17:42:25.105708');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cart_cart
-- ----------------------------
DROP TABLE IF EXISTS `cart_cart`;
CREATE TABLE `cart_cart`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `quantity` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `goods_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `cart_cart_user_id_goods_id_93dafe04_uniq`(`user_id`, `goods_id`) USING BTREE,
  INDEX `cart_cart_goods_id_57b72e23_fk_goods_goods_id`(`goods_id`) USING BTREE,
  CONSTRAINT `cart_cart_goods_id_57b72e23_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `cart_cart_user_id_9b4220b9_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cart_cart
-- ----------------------------
INSERT INTO `cart_cart` VALUES (1, 1, '2026-06-27 17:42:25.311292', 8, 2);
INSERT INTO `cart_cart` VALUES (2, 1, '2026-06-27 17:42:25.313795', 2, 2);
INSERT INTO `cart_cart` VALUES (3, 1, '2026-06-27 17:42:25.315805', 5, 3);
INSERT INTO `cart_cart` VALUES (4, 1, '2026-06-27 17:42:25.316805', 2, 3);
INSERT INTO `cart_cart` VALUES (5, 1, '2026-06-27 17:42:25.318805', 1, 4);
INSERT INTO `cart_cart` VALUES (6, 1, '2026-06-27 17:42:25.320806', 2, 4);

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (10, 'cart', 'cart');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (12, 'favorite', 'favorite');
INSERT INTO `django_content_type` VALUES (8, 'goods', 'category');
INSERT INTO `django_content_type` VALUES (9, 'goods', 'goods');
INSERT INTO `django_content_type` VALUES (13, 'message', 'message');
INSERT INTO `django_content_type` VALUES (11, 'order', 'order');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (7, 'users', 'userprofile');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2026-06-27 17:40:34.923286');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2026-06-27 17:40:35.241317');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2026-06-27 17:40:35.311454');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2026-06-27 17:40:35.317961');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2026-06-27 17:40:35.324586');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2026-06-27 17:40:35.366691');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2026-06-27 17:40:35.401770');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2026-06-27 17:40:35.413236');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2026-06-27 17:40:35.419339');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2026-06-27 17:40:35.449038');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2026-06-27 17:40:35.452038');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2026-06-27 17:40:35.459250');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2026-06-27 17:40:35.468294');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2026-06-27 17:40:35.475803');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2026-06-27 17:40:35.487799');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2026-06-27 17:40:35.492959');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2026-06-27 17:40:35.500510');
INSERT INTO `django_migrations` VALUES (18, 'auth', '0013_create_custom_user', '2026-06-27 17:40:35.502013');
INSERT INTO `django_migrations` VALUES (19, 'goods', '0001_initial', '2026-06-27 17:40:35.606632');
INSERT INTO `django_migrations` VALUES (20, 'cart', '0001_initial', '2026-06-27 17:40:35.688965');
INSERT INTO `django_migrations` VALUES (21, 'favorite', '0001_initial', '2026-06-27 17:40:35.775698');
INSERT INTO `django_migrations` VALUES (22, 'message', '0001_initial', '2026-06-27 17:40:35.859135');
INSERT INTO `django_migrations` VALUES (23, 'order', '0001_initial', '2026-06-27 17:40:35.999591');
INSERT INTO `django_migrations` VALUES (24, 'sessions', '0001_initial', '2026-06-27 17:40:36.025907');
INSERT INTO `django_migrations` VALUES (25, 'users', '0001_initial', '2026-06-27 17:40:36.092036');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('220mr10h28emg60ykz0nvqd4bzcv8lb6', '.eJyVVMGSmzAM_ZUM5yQLxjZmj733C8pOxtgyoUswg2Hbzk7-vQgyaQAn2V4sbIn3JD3Zn8FB9t3x0DtoD6UOXoMo2N6e5VK9Q40O_VPWhd0rW3dtme8xZH_xuv13q6H6domdARylOw5_GyCMCwosAWFSKlKihUp1DBCG-WAVi6lMITWEpIMTUg40N2wgCCNF8hRBT1D3bsD68ZkFsmmy4HWTBYW12mXBdvis5QmmwyzrGaMcDVXRYJJcjoaGfIothzqmWCPdxshdbn9PnhOW4tCHPA8wGYmSwQjBxRoTIavSdZOnb6vJ8SL1qaxfxqQv6xQBpcaIKAzJebt5RhziLlFJ7ifuZOEeESvZQWHbPyvu-PyGB4dfUBbHDg_DeUA0JXftvm01tJ7uU5B0MJxH8Ze67462acq62CnZdk91ELkk2IeYsWfoCN6CgrK5I8VYwWVdtoN5pBCaaGQjPMWd4XdIrxXl0r3DHXKsdlqW1NxDzVmMugumzGImvBkc4drLJa-RH7YtO_j3seRPVpMQzQPoYhLwsvvuYcKIwNxJnHxpEm5wHkzAHJUaQFQecuNvBYL6OzHSjWvTWlNW606kHiUSqVF9FgkcQK6FeEgP9QdUtgF_CidwThZwtYsEonAlBZlnKBZS4OPrUWK4NXQ00yNChcKk4yn3hMZ3r2YJld7J6vm9vFXlP3XAnEcZVuX73sMEFL3P4HbKFg9oitb2zYpn_fbF84Do_Bac_wJrXS-9:1wf5e3:39iXcVUGdgETywyt_0oC58blsDQPp2J1UgenLGB45hA', '2026-07-16 00:51:11.446105');
INSERT INTO `django_session` VALUES ('8pex5p5j9ul8i294wsczesy9tkmxab8y', '.eJyVVMGSmzAM_ZUM5yQLxjZmj733C8pOxtgyoUswg2Hbzk7-vQgyaQAn2V4sbIn3JD3Zn8FB9t3x0DtoD6UOXoMo2N6e5VK9Q40O_VPWhd0rW3dtme8xZH_xuv13q6H6domdARylOw5_GyCMCwosAWFSKlKihUp1DBCG-WAVi6lMITWEpIMTUg40N2wgCCNF8hRBT1D3bsD68ZkFsmmy4HWTBYW12mXBdvis5QmmwyzrGaMcDVXRYJJcjoaGfIothzqmWCPdxshdbn9PnhOW4tCHPA8wGYmSwQjBxRoTIavSdZOnb6vJ8SL1qaxfxqQv6xQBpcaIKAzJebt5RhziLlFJ7ifuZOEeESvZQWHbPyvu-PyGB4dfUBbHDg_DeUA0JXftvm01tJ7uU5B0MJxH8Ze67462acq62CnZdk91ELkk2IeYsWfoCN6CgrK5I8VYwWVdtoN5pBCaaGQjPMWd4XdIrxXl0r3DHXKsdlqW1NxDzVmMugumzGImvBkc4drLJa-RH7YtO_j3seRPVpMQzQPoYhLwsvvuYcKIwNxJnHxpEm5wHkzAHJUaQFQecuNvBYL6OzHSjWvTWlNW606kHiUSqVF9FgkcQK6FeEgP9QdUtgF_CidwThZwtYsEonAlBZlnKBZS4OPrUWK4NXQ00yNChcKk4yn3hMZ3r2YJld7J6vm9vFXlP3XAnEcZVuX73sMEFL3P4HbKFg9oitb2zYpn_fbF84Do_Bac_wJrXS-9:1wf5mW:BnLFJhyamstLHQsxPls3ohi6sTVnxBGrvNppAzetNOg', '2026-07-16 00:59:56.940186');
INSERT INTO `django_session` VALUES ('bb867vvq69g1x441m3tcvfjb5ick56t9', '.eJyVVMGSmzAM_ZUM5yQLxjZmj733C8pOxtgyoUswg2Hbzk7-vQgyaQAn2V4sbIn3JD3Zn8FB9t3x0DtoD6UOXoMo2N6e5VK9Q40O_VPWhd0rW3dtme8xZH_xuv13q6H6domdARylOw5_GyCMCwosAWFSKlKihUp1DBCG-WAVi6lMITWEpIMTUg40N2wgCCNF8hRBT1D3bsD68ZkFsmmy4HWTBYW12mXBdvis5QmmwyzrGaMcDVXRYJJcjoaGfIothzqmWCPdxshdbn9PnhOW4tCHPA8wGYmSwQjBxRoTIavSdZOnb6vJ8SL1qaxfxqQv6xQBpcaIKAzJebt5RhziLlFJ7ifuZOEeESvZQWHbPyvu-PyGB4dfUBbHDg_DeUA0JXftvm01tJ7uU5B0MJxH8Ze67462acq62CnZdk91ELkk2IeYsWfoCN6CgrK5I8VYwWVdtoN5pBCaaGQjPMWd4XdIrxXl0r3DHXKsdlqW1NxDzVmMugumzGImvBkc4drLJa-RH7YtO_j3seRPVpMQzQPoYhLwsvvuYcKIwNxJnHxpEm5wHkzAHJUaQFQecuNvBYL6OzHSjWvTWlNW606kHiUSqVF9FgkcQK6FeEgP9QdUtgF_CidwThZwtYsEonAlBZlnKBZS4OPrUWK4NXQ00yNChcKk4yn3hMZ3r2YJld7J6vm9vFXlP3XAnEcZVuX73sMEFL3P4HbKFg9oitb2zYpn_fbF84Do_Bac_wJrXS-9:1weEGX:_6L6Mco-TAgkyVJqd1PnEnmmIlP86rPbVUgZorsWalQ', '2026-07-13 15:51:21.664714');
INSERT INTO `django_session` VALUES ('quihd7g7xh6ng00r9fcw53tejoip2lmx', '.eJyVVMGSmzAM_ZUM5yQLxjZmj733C8pOxtgyoUswg2Hbzk7-vQgyaQAn2V4sbIn3JD3Zn8FB9t3x0DtoD6UOXoMo2N6e5VK9Q40O_VPWhd0rW3dtme8xZH_xuv13q6H6domdARylOw5_GyCMCwosAWFSKlKihUp1DBCG-WAVi6lMITWEpIMTUg40N2wgCCNF8hRBT1D3bsD68ZkFsmmy4HWTBYW12mXBdvis5QmmwyzrGaMcDVXRYJJcjoaGfIothzqmWCPdxshdbn9PnhOW4tCHPA8wGYmSwQjBxRoTIavSdZOnb6vJ8SL1qaxfxqQv6xQBpcaIKAzJebt5RhziLlFJ7ifuZOEeESvZQWHbPyvu-PyGB4dfUBbHDg_DeUA0JXftvm01tJ7uU5B0MJxH8Ze67462acq62CnZdk91ELkk2IeYsWfoCN6CgrK5I8VYwWVdtoN5pBCaaGQjPMWd4XdIrxXl0r3DHXKsdlqW1NxDzVmMugumzGImvBkc4drLJa-RH7YtO_j3seRPVpMQzQPoYhLwsvvuYcKIwNxJnHxpEm5wHkzAHJUaQFQecuNvBYL6OzHSjWvTWlNW606kHiUSqVF9FgkcQK6FeEgP9QdUtgF_CidwThZwtYsEonAlBZlnKBZS4OPrUWK4NXQ00yNChcKk4yn3hMZ3r2YJld7J6vm9vFXlP3XAnEcZVuX73sMEFL3P4HbKFg9oitb2zYpn_fbF84Do_Bac_wJrXS-9:1wdX6Y:2h3Ei_bi528HiSyizIqFrS7hk5svLx2X_LUX1NAqKeQ', '2026-07-11 17:46:10.438123');

-- ----------------------------
-- Table structure for favorite_favorite
-- ----------------------------
DROP TABLE IF EXISTS `favorite_favorite`;
CREATE TABLE `favorite_favorite`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `goods_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `favorite_favorite_user_id_goods_id_5be56bdb_uniq`(`user_id`, `goods_id`) USING BTREE,
  INDEX `favorite_favorite_goods_id_2aafb2d6_fk_goods_goods_id`(`goods_id`) USING BTREE,
  CONSTRAINT `favorite_favorite_goods_id_2aafb2d6_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `favorite_favorite_user_id_d75a5c08_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of favorite_favorite
-- ----------------------------
INSERT INTO `favorite_favorite` VALUES (1, '2026-06-27 17:42:25.323309', 3, 2);
INSERT INTO `favorite_favorite` VALUES (2, '2026-06-27 17:42:25.325325', 4, 2);
INSERT INTO `favorite_favorite` VALUES (3, '2026-06-27 17:42:25.327325', 5, 3);
INSERT INTO `favorite_favorite` VALUES (4, '2026-06-27 17:42:25.329443', 8, 3);
INSERT INTO `favorite_favorite` VALUES (5, '2026-06-27 17:42:25.330959', 7, 3);
INSERT INTO `favorite_favorite` VALUES (6, '2026-06-27 17:42:25.332960', 1, 4);
INSERT INTO `favorite_favorite` VALUES (7, '2026-06-27 17:42:25.334464', 8, 4);
INSERT INTO `favorite_favorite` VALUES (8, '2026-06-27 17:42:25.335465', 3, 5);
INSERT INTO `favorite_favorite` VALUES (9, '2026-06-27 17:42:25.337465', 6, 5);
INSERT INTO `favorite_favorite` VALUES (10, '2026-06-27 17:42:25.338466', 7, 5);
INSERT INTO `favorite_favorite` VALUES (11, '2026-06-27 17:42:25.340466', 8, 6);
INSERT INTO `favorite_favorite` VALUES (12, '2026-06-27 17:42:25.341466', 2, 6);

-- ----------------------------
-- Table structure for goods_category
-- ----------------------------
DROP TABLE IF EXISTS `goods_category`;
CREATE TABLE `goods_category`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `icon` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `sort` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `parent_id` bigint(20) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `goods_category_parent_id_c69c7899_fk_goods_category_id`(`parent_id`) USING BTREE,
  CONSTRAINT `goods_category_parent_id_c69c7899_fk_goods_category_id` FOREIGN KEY (`parent_id`) REFERENCES `goods_category` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of goods_category
-- ----------------------------
INSERT INTO `goods_category` VALUES (1, '数码产品', NULL, 0, 1, '2026-06-27 17:40:46.622518', NULL);
INSERT INTO `goods_category` VALUES (2, '服饰鞋包', NULL, 0, 1, '2026-06-27 17:40:46.624623', NULL);
INSERT INTO `goods_category` VALUES (3, '家居生活', NULL, 0, 1, '2026-06-27 17:40:46.627828', NULL);
INSERT INTO `goods_category` VALUES (4, '图书文具', NULL, 0, 1, '2026-06-27 17:40:46.629829', NULL);
INSERT INTO `goods_category` VALUES (5, '运动户外', NULL, 0, 1, '2026-06-27 17:40:46.631829', NULL);
INSERT INTO `goods_category` VALUES (6, '母婴用品', NULL, 0, 1, '2026-06-27 17:40:46.633332', NULL);

-- ----------------------------
-- Table structure for goods_goods
-- ----------------------------
DROP TABLE IF EXISTS `goods_goods`;
CREATE TABLE `goods_goods`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  `original_price` decimal(10, 2) NULL DEFAULT NULL,
  `cover_image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `images` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `view_count` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category_id` bigint(20) NULL DEFAULT NULL,
  `seller_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `goods_goods_category_id_da3507dd_fk_goods_category_id`(`category_id`) USING BTREE,
  INDEX `goods_goods_seller_id_dd387ea8_fk_auth_user_id`(`seller_id`) USING BTREE,
  CONSTRAINT `goods_goods_category_id_da3507dd_fk_goods_category_id` FOREIGN KEY (`category_id`) REFERENCES `goods_category` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `goods_goods_seller_id_dd387ea8_fk_auth_user_id` FOREIGN KEY (`seller_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of goods_goods
-- ----------------------------
INSERT INTO `goods_goods` VALUES (1, 'iPhone 13 Pro 二手 95新', 'iPhone 13 Pro 256GB，外观完好，功能正常，电池健康85%', 4599.00, 6999.00, 'goods/covers/goods_1.jpg', NULL, 'on_sale', 82, '2026-06-27 17:42:25.295181', '2026-07-02 00:56:42.173574', 1, 2);
INSERT INTO `goods_goods` VALUES (2, 'MacBook Pro 16寸 2021', 'M1 Pro芯片，16G内存，512G固态，带原装充电器', 12999.00, 18999.00, 'goods/covers/goods_2.jpg', NULL, 'on_sale', 76, '2026-06-27 17:42:25.297182', '2026-07-02 00:56:43.789410', 1, 2);
INSERT INTO `goods_goods` VALUES (3, 'Nike Air Max 运动鞋 42码', '9成新，仅穿过几次，原盒包装', 399.00, 799.00, 'goods/covers/goods_3.jpg', NULL, 'on_sale', 35, '2026-06-27 17:42:25.299774', '2026-07-02 00:56:45.558484', 2, 2);
INSERT INTO `goods_goods` VALUES (4, '优衣库羽绒服 男款 L码', '黑色，轻薄保暖，穿过一个冬季', 299.00, 599.00, 'goods/covers/goods_4.jpg', NULL, 'on_sale', 111, '2026-06-27 17:42:25.300774', '2026-07-02 00:56:47.313021', 2, 2);
INSERT INTO `goods_goods` VALUES (5, '小米空气净化器 Pro H', '使用半年，功能完好，滤芯剩余50%', 599.00, 1299.00, 'goods/covers/goods_5.jpg', NULL, 'on_sale', 175, '2026-06-27 17:42:25.303278', '2026-07-02 00:56:49.060403', 3, 3);
INSERT INTO `goods_goods` VALUES (6, 'Python编程从入门到实践', '几乎全新，无笔记划痕', 39.00, 89.00, 'goods/covers/goods_6.jpg', NULL, 'on_sale', 119, '2026-06-27 17:42:25.304292', '2026-07-02 00:56:50.587966', 4, 3);
INSERT INTO `goods_goods` VALUES (7, '迪卡侬登山背包 30L', '蓝色，防水材质，仅用过一次', 129.00, 299.00, 'goods/covers/goods_7.jpg', NULL, 'on_sale', 122, '2026-06-27 17:42:25.306292', '2026-07-02 00:56:52.138979', 5, 3);
INSERT INTO `goods_goods` VALUES (8, '婴儿推车 可坐可躺', '9成新，宝宝大了用不上了，功能完好', 399.00, 899.00, 'goods/covers/goods_8.jpg', NULL, 'on_sale', 36, '2026-06-27 17:42:25.308291', '2026-07-02 00:56:53.773456', 6, 4);

-- ----------------------------
-- Table structure for message_message
-- ----------------------------
DROP TABLE IF EXISTS `message_message`;
CREATE TABLE `message_message`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `message_message_receiver_id_dc38e7dd_fk_auth_user_id`(`receiver_id`) USING BTREE,
  INDEX `message_message_sender_id_b8690ab2_fk_auth_user_id`(`sender_id`) USING BTREE,
  CONSTRAINT `message_message_receiver_id_dc38e7dd_fk_auth_user_id` FOREIGN KEY (`receiver_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `message_message_sender_id_b8690ab2_fk_auth_user_id` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for order_order
-- ----------------------------
DROP TABLE IF EXISTS `order_order`;
CREATE TABLE `order_order`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `order_no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `pay_time` datetime(6) NULL DEFAULT NULL,
  `ship_time` datetime(6) NULL DEFAULT NULL,
  `complete_time` datetime(6) NULL DEFAULT NULL,
  `buyer_id` int(11) NOT NULL,
  `goods_id` bigint(20) NOT NULL,
  `seller_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `order_no`(`order_no`) USING BTREE,
  INDEX `order_order_buyer_id_dadf595a_fk_auth_user_id`(`buyer_id`) USING BTREE,
  INDEX `order_order_goods_id_b8ae2ba1_fk_goods_goods_id`(`goods_id`) USING BTREE,
  INDEX `order_order_seller_id_003495e4_fk_auth_user_id`(`seller_id`) USING BTREE,
  CONSTRAINT `order_order_buyer_id_dadf595a_fk_auth_user_id` FOREIGN KEY (`buyer_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `order_order_goods_id_b8ae2ba1_fk_goods_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods_goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `order_order_seller_id_003495e4_fk_auth_user_id` FOREIGN KEY (`seller_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for users_userprofile
-- ----------------------------
DROP TABLE IF EXISTS `users_userprofile`;
CREATE TABLE `users_userprofile`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `avatar` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `nickname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `users_userprofile_user_id_87251ef1_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users_userprofile
-- ----------------------------
INSERT INTO `users_userprofile` VALUES (1, '13818841420', '', '小明', '北京市朝阳区某某街道123号', '2026-06-27 17:42:24.530083', 2);
INSERT INTO `users_userprofile` VALUES (2, '13855420707', '', '小红', '北京市朝阳区某某街道123号', '2026-06-27 17:42:24.728559', 3);
INSERT INTO `users_userprofile` VALUES (3, '13815882736', '', '张三', '北京市朝阳区某某街道123号', '2026-06-27 17:42:24.919569', 4);
INSERT INTO `users_userprofile` VALUES (4, '13826986022', '', '李四', '北京市朝阳区某某街道123号', '2026-06-27 17:42:25.103222', 5);
INSERT INTO `users_userprofile` VALUES (5, '13851209627', '', '王五', '北京市朝阳区某某街道123号', '2026-06-27 17:42:25.287668', 6);
INSERT INTO `users_userprofile` VALUES (6, NULL, '', NULL, NULL, '2026-06-27 17:45:44.530000', 1);

SET FOREIGN_KEY_CHECKS = 1;
