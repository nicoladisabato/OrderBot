##### Schema creation #####
CREATE TABLE products (
	product_id INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    product_description VARCHAR(256) NOT NULL,
    product_ingredients VARCHAR(256) null,
    product_price FLOAT NOT NULL,
    product_type VARCHAR(64) NOT NULL,
	available BOOLEAN NOT NULL,
    PRIMARY KEY (product_id)
);



INSERT INTO products VALUES 
(0, 'Margherita', 'Classic and timeless', 'tomato, mozzarella, oil, basil', 4.5, 'pizza', 1),
(1, 'Diavola', 'spicy pizza with a strong taste', 'tomato, mozzarella, pepperoni', 6.0, 'pizza', 1),
(2, 'Marinara', 'very simple and vegan', 'tomato, garlic, origan, oil', 4.0, 'pizza', 1),
(3, 'Vegetarian', 'vegetarian with vegetables', 'grilled courgettes and aubergines', 6.0, 'pizza', 1),
(4, 'Fanta', '33cl. can', NULL, 3.0, 'drink', 1),
(5, 'Coca-cola', '33cl. can', NULL, 3.0, 'drink', 1),
(6, 'Water', '100cl bottle of water', NULL, 2.0, 'drink', 1);


### stored procedure ####
DELIMITER $$
CREATE PROCEDURE get_price (IN product_name VARCHAR(100))
BEGIN
    DECLARE result DECIMAL(3,2);
    
    IF product_name <> '' THEN
        SELECT product_price INTO result
        FROM products
        WHERE LOWER(products.product_name) = LOWER(product_name);
    END IF;
    
	-- Handling when no records are found
    IF result IS NULL THEN
        SET result = -1;
    END IF;

    SELECT result AS price;
END$$
DELIMITER ;



### stored procedure ####
DELIMITER $$

CREATE PROCEDURE get_ingredients_and_description (IN product_name VARCHAR(100))
BEGIN
    DECLARE result_ingredients VARCHAR(256);
    DECLARE result_description VARCHAR(256);
    
    -- Get ingredients and description for the given product_name
    SELECT product_ingredients, product_description
    INTO result_ingredients, result_description
    FROM products
    WHERE LOWER(products.product_name) = LOWER(product_name);
    
    -- Handling when no records are found
    IF result_ingredients IS NULL THEN
        SET result_ingredients = -1;
    END IF;

    -- Return ingredients and description
    SELECT result_ingredients AS ingredients, result_description AS description;
END$$

DELIMITER ;



### stored procedure ####
DELIMITER $$

CREATE PROCEDURE check_availability (IN product_name VARCHAR(100))
BEGIN
    DECLARE product_availability INT;

    SELECT available INTO product_availability
    FROM products
    WHERE LOWER(products.product_name) = LOWER(product_name);

    SELECT product_availability AS result;
END$$

DELIMITER ;



### stored procedure ####
DELIMITER //
CREATE PROCEDURE get_product_menu (
    IN p_product_name VARCHAR(255),
    IN p_product_type VARCHAR(255)
)
BEGIN
    SELECT product_name, product_ingredients, product_price
    FROM products
    WHERE (p_product_name = '' OR product_name = p_product_name)
    AND (p_product_type = '' OR product_type = p_product_type) 
    AND available;
END //
DELIMITER ;




###########################################

-- Create Orders Table
CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATETIME);

-- Create Order_Items Table
CREATE TABLE Order_Items (
    order_id INT,
    product_name VARCHAR(255),
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

DELIMITER //

-- Create a new stored procedure to add an order
CREATE PROCEDURE create_order (
    IN p_order_date DATE
)
BEGIN
    -- Insert a new row into the orders table
    INSERT INTO orders (order_date)
    VALUES (p_order_date);
END //

DELIMITER ;







###############################

##### Schema creation #####
CREATE TABLE Beers (
	product_id INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    description VARCHAR(256),
    country VARCHAR(50) NOT NULL,
    style VARCHAR(100),
    alcohol_content FLOAT,
    ibu_value INT,
    PRIMARY KEY (product_id)
);


INSERT INTO Beers VALUES 
(0, 'PUNK IPA', 'Aromatic burst of tropical fruits & citrus (grapefruit, lychee, pineapple). Exotic, fruity taste with balanced malt & hops, ending in a long fragrant finish.', 'Scotland', 'India pale ale', 5.6, 35),
(1, 'QUARANTOT', 'Aromas of caramel, biscuit & honey blend with fruity (peach, mango), floral (jasmine), & woody notes. Sweet start leads to balanced finish, avoiding excessive bitterness.', 'Italy, Milan', 'Double IPA', 8, 140),
(2, 'ESTRELLA GALICIA GLUTEN FREE', 'in the mouth it has a neutral and light taste with a marked hoppy note.', 'Spain', 'Special Lager (Gluten Free)', 4.5, 25);


-- Create the get_beers procedure
DELIMITER //
CREATE PROCEDURE `get_beers`(IN beer_name VARCHAR(100))
BEGIN
    IF beer_name <> '' THEN 
		SELECT product_name, country, style, alcohol_content, ibu_value 
        FROM Beers
        WHERE LOWER(product_name) = LOWER(beer_name);
        
	ELSE SELECT product_name, country, style, alcohol_content, ibu_value 
        FROM Beers;
	END IF;
END
DELIMITER ;