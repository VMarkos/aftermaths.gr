class Post
    @ALIGN_CENTER   = "has-text-align-center"
    @LATEX          = "LATEX"

    def initialize(filename)
        @file = File.new(filename, "r")
        @current_line = nil
        @current_char = ""
        @previous_char = nil
        @current_index = 0 # eagerly points to the next element to be consumed
        @current_class = nil
        @current_tag = nil
        @modified_file = ""
        @modified_line = nil
        @modifying = false
    end

    def _advance()
        @previous_char = @current_char
        @current_char = @current_line[@current_index]
        @current_index += 1
        if not @modifying
            @modified_line += @current_char
        end
    end

    def _peek(n = 1)
        temp_index = @current_index
        temp_char = @current_char
        peeked_str = temp_char
        i = 1
        while @temp_char != "\n" and i < n
            peeked_str += temp_char
            temp_index += 1
            temp_char = @current_line[temp_index]
            i += 1
        end
        return peeked_str
    end

    def _is_at_end()
      return @current_char == "\n"
    end

    def _change_line(line)
        @current_line = line
        @current_index = 0
        @current_char = @current_line[@current_index]
        @previous_char = nil
        @modified_line = ""
    end

    def fix_math()
        # Spots $latex ...$ and substitutes it by $...$ with the exception of centered math (display)
        @file.each_line do |line|
            _change_line(line)
            while not _is_at_end
                case @current_char
                when "$"
                    _consume_math
                when "<" # TODO You have to keep track of tags etc and put them into the modified line!
                    if _peek == "/"
                        _advance # consume "/"
                        _consume_tag_end
                    else
                        _consume_tag_start
                    end        
                end
                _advance
            end
        end
    end

    def _is_in_centered_par()
        return (@current_tag == "p" and @current_class == @ALIGN_CENTER)
    end

    def _consume_math()
        # In case this is a dollar sign that does not start math, i.e.:
        #   * not followed by "latex", or;
        #   * preceeded by "\".
        return if _peek(5) != @LATEX or @previous_char == "\\"
        @modifying = true
        if _is_in_centered_par
            # Handle the case of displayed math here!
            _skip(6) # consume "$latex"
            math_content = _consume_math_content
            _advance # consume $
            _advance # consume $
            # FIXME "\displaystyle" has survived here
            @modified_line += "$$#{math_content}$$"
        else
            _skip(5) # consume "latex"
            math_content = _consume_math_content
            _advance # consume $
            @modified_line += "$#{math_content}$"
        end
        @modifying = false
    end

    def _consume_math_content()
        math_content = ""
        while not _is_at_end and (@current_char != "$" or @previous_char == "\\")
            math_content += @current_char
            _advance
        end
        return math_content
    end

    def _consume_tag_end()
        tag_name = _get_tag_name
        if tag_name != @current_tag
            raise "Unmatched tag name!"
        end
        # @modified_line += "</#{@current_tag}>"
        # reset class and tag
        @current_tag = nil
        @current_class = nil
        _advance
    end

    def _consume_tag_start()
        # TODO copy all contents to modified line
        tag_name = _get_tag_name
        @current_tag = tag_name
        # @modified_line += "<#{tag_name}"
        while @current_char != ">"
            _consume_space
            _consume_class
        end
        # @modified_line += ">"
    end

    def _get_tag_name()
        tag_name = ""
        while not _is_at_end and @current_char != " " and @current_char != ">"
            tag_name += @current_char
            _advance
        end
        return tag_name
    end

    def _consume_space()
        while not _is_at_end and @current_char == " "
            _advance
        end
    end

    def _skip(n = 1)
        # better use for n > 1
        n.times do
            _advance
        end
    end

    def _consume_class()
        return if _peek(5) != "class"
        # consume spaces and "=" until we reach "
        _skip(5)
        classname = ""
        while not _is_at_end and @current_char != "\""
            classname += @current_char
            _advance
        end
        @current_class = classname
        _advance
    end

    def rows
        count = 0
        @file.each_line do |line|
            count += 1
        end
        return count
    end
end

if __FILE__ == $0
    PATH = File.expand_path File.dirname(__FILE__)
    POSTS_PATH = File.join(PATH, "_posts")
    puts "CWD: #{POSTS_PATH}"
    
    posts_processed = 0
    Dir.foreach(POSTS_PATH) do |filename|
        next if filename == "." or filename == ".."
        post = Post.new(File.join(POSTS_PATH, filename))
        print "Post rows: #{post.rows}\r"
        posts_processed += 1
    end
    puts "Posts processed: #{posts_processed}."
end