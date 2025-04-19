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
        @modified_file = ""
        @modified_line = nil
    end

    def _advance()
        @previous_char = @current_char
        @current_char = @current_line[@current_index]
        @current_index += 1
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

    def _change_line(line)
        @current_line = line
        @current_index = 0
        @current_char = @current_line[@current_index]
        @previous_char = nil
        @modified_line = ""
    end

    def fix_math:
        # Spots $latex ...$ and substitutes it by $...$ with the exception of centered math (display)
        @file.each_line do |line|
            _change_line(line)
            while @current_char != "\n"
                case @current_char
                when "$"
                    _consume_math
                when "<"
                    _consume_tag
                end
                _advance
            end
        end
    end

    def _consume_math()
        # In case this is a dollar sign that does not start math, i.e.:
        #   * not followed by "latex", or;
        #   * preceeded by "\".
        return if _peek(5) != @LATEX or @previous_char == "\\"
        if @current_class == @ALIGN_CENTER
            # Handle the case of displayed math here!
        else
            5.times do # consume "latex"
                _advance
            end
            math_content = ""
            while @current_char != "$" or @previous_char == "\\"
                math_content += @current_char
                _advance
            end
            @modified_line += "$#{math_content}$"
        end
    end

    def _consume_tag()
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